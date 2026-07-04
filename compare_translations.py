#!/usr/bin/python3

import csv
from pathlib import Path
from collections import defaultdict

import yaml

def load_csv_data(csv_path):
  overrides = []
  with open(csv_path) as f:
    reader = csv.DictReader(f)
    for row in reader:
      overrides.append({
        'locale': row['locale'],
        'key': row['translation_key'],
        'override_value': row['value'],
        'original_value': row['original_translation'],
        'status': row['status']
      })
  return overrides

def flatten_yaml(data, parent_key='', sep='.'):
  """Flatten nested YAML structure to dot-notation keys."""
  items = {}
  if isinstance(data, dict):
    for key, value in data.items():
      new_key = f"{parent_key}{sep}{key}" if parent_key else str(key)
      if isinstance(value, dict):
        items.update(flatten_yaml(value, new_key, sep))
      else:
        items[new_key] = value
  return items

def load_translation_files(locales_dir, locales):
  """Load all translation files and organize by locale."""
  translations = defaultdict(dict)
  if locales is not None:
    locales = locales.split(',')

  for file_path in Path(locales_dir).glob('**/*.yml'):
    filename = file_path.name
    # Extract locale from filename (e.g., server.en.yml -> en, client.zh_CN.yml -> zh_CN)
    parts = filename.split('.')
    if len(parts) < 3:
      continue

    locale = parts[1]
    if locale not in locales:
      continue

    with open(file_path) as f:
      data = yaml.safe_load(f)
      # Flatten the YAML structure
      flattened = flatten_yaml(data)
      # Remove the top-level locale key if present
      for key, value in flattened.items():
        # Remove prefix like "en." or "zh_CN."
        if key.startswith(f"{locale}."):
          clean_key = key[len(locale)+1:]
          translations[locale][clean_key] = value
        else:
          translations[locale][key] = value

  return translations

def compare_translations(overrides, translations):
  """Compare override values with source translations."""
  same = []
  different = []
  not_found = []

  for override in overrides:
    locale = override['locale']
    key = override['key']
    override_value = override['override_value']

    # Look up the key in source translations
    source_value = translations.get(locale, {}).get(key)

    if source_value is None:
      not_found.append({
        'key': key,
        'locale': locale,
        'override_value': override_value
      })
    elif str(source_value) == override_value:
      same.append({
        'key': key,
        'locale': locale,
        'value': override_value
      })
    else:
      different.append({
        'key': key,
        'locale': locale,
        'source_value': str(source_value),
        'override_value': override_value
      })

  return same, different, not_found

def main():
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument('--locales',
                     help='limit locales to this comma-separated list')
  parser.add_argument('csv_path')
  parser.add_argument('discourse_path')
  args = parser.parse_args()

  # Paths
  csv_path = args.csv_path
  locales_dir = args.discourse_path

  print("Loading translation overrides from CSV...")
  overrides = load_csv_data(csv_path)
  print(f"Found {len(overrides)} overrides")

  print("\nLoading translation files...")
  translations = load_translation_files(locales_dir, args.locales)
  print(f"Loaded translations for {len(translations)} locales")

  print("\nComparing translations...")
  same, different, not_found = compare_translations(overrides, translations)

  # Output results
  print("\n" + "="*80)
  print("KEYS THAT ARE NOW THE SAME")
  print("="*80)
  if same:
    for item in same:
      print(f"[{item['locale']}] {item['key']}")
    print()
  else:
    print("None\n")

  print("="*80)
  print("KEYS THAT ARE DIFFERENT")
  print("="*80)
  if different:
    for item in different:
      print(f"[{item['locale']}] {item['key']}")
      print(f"  Source: {item['source_value']}")
      print(f"  Override: {item['override_value']}")
      print()
  else:
    print("None\n")

  print("="*80)
  print("KEYS NOT FOUND IN SOURCE")
  print("="*80)
  if not_found:
    for item in not_found:
      print(f"[{item['locale']}] {item['key']}")
      print(f"  Override value: {item['override_value']}")
      print()
  else:
    print("None\n")

  print("="*80)
  print("SUMMARY")
  print("="*80)
  print(f"Total overrides: {len(overrides)}")
  print(f"Same as source: {len(same)}")
  print(f"Different from source: {len(different)}")
  print(f"Not found in source: {len(not_found)}")

if __name__ == '__main__':
  main()
