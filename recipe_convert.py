#!/usr/bin/env python3

import sys
import json
import argparse
import re
from os.path import basename, splitext, join as path_join

def get_json(filepath):
    with open(filepath) as file:
        return json.load(file), filepath

def dump_md(recipe):
    ingredients = [
        re.sub('\s\s+', ' ', '{} {} {}'
            .format(ingredient['amount'], ingredient['unit'], ingredient['name']))
        for ingredient
        in recipe['ingredients']
    ]

    ingredient_list = '\n'.join('- {}'.format(list_item) for list_item in ingredients)

    md_lines = [
        '# ' + recipe['title'],
        'Meal: _{}_, Course: _{}_'.format(recipe['meal'], recipe['course']),
        '## Ingredients',
        ingredient_list,
        '## Directions' if recipe['directions'] else '',
        recipe['directions'],
        '## Notes' if recipe['notes'] else '',
        recipe['notes'],
    ]
    return '\n\n'.join(md_lines)


DEFAULT_SERIALIZER = 'md'
SERIALIZERS = {
    'md': dump_md
}

arg_parser = argparse.ArgumentParser()

arg_parser.add_argument('-f', '--format', 
                        help='output conversion format',
                        choices=SERIALIZERS.keys(), 
                        default=DEFAULT_SERIALIZER)

arg_parser.add_argument('-o', '--output-dir', 
                        help='directory to output the files',
                        default='.')

arg_parser.add_argument('recipes',
                        metavar='RECIPE_FILE', 
                        help='recipe file in a JSON format', 
                        type=get_json, 
                        nargs='+')

args = arg_parser.parse_args()

for recipe, filepath in args.recipes:
    serializer = SERIALIZERS[args.format]
    output = serializer(recipe)
    output_filename = splitext(basename(filepath))[0] + '.' + args.format
    write_file = open(path_join(args.output_dir, output_filename), 'w')
    write_file.write(output)
    write_file.close()