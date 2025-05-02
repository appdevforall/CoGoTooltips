#! /usr/bin/python

import json
import os
import os.path as path
from pprint import pformat
import sqlite3
import sys


JSON_FILE         = "CoGoTooltips.json"
DATABASE_FILENAME = "/home/david/Documentation.db"
TOOLTIP_TABLE     = "ide_tooltip_table"
TOOLTIP_COLUMNS   = ("tooltipTag", "tooltipSummary", "tooltipDetail", "tooltipButtons")
INSERT_SQL        = f"""INSERT INTO {TOOLTIP_TABLE} ({", ".join(TOOLTIP_COLUMNS)}) VALUES (?, ?, ?, ?);"""



# ------------------------------------------------------------------------------
# A sample item:
#  
#   {'buttons': [['Learn more about module java.base',
#                 'file:///android_asset/CoGoTooltips/external/javadocs/api/java.base/module-summary.html']],
#    'category': 'java',
#    'detail': 'Defines the foundational APIs of the Java SE Platform.\n'
#              '\n'
#              ' <dl class="notes"><dt>Providers:</dt><dd> The JDK implementation '
#              'of this module provides an implementation of the <span '
#              'class="search-tag-result" id="jrt">jrt</span> <a '
#              'href="java/nio/file/spi/FileSystemProvider.html" title="class in '
#              'java.nio.file.spi">file system provider</a> to enumerate and read '
#              'the class and resource files in a run-time image. The jrt file '
#              'system can be created by calling <a '
#              'href="java/nio/file/FileSystems.html#newFileSystem(java.net.URI,java.util.Map)"><code>FileSystems.newFileSystem(URI.create("jrt:/"))</code></a>. '
#              '</dd></dl>',
#    'summary': 'Defines the foundational APIs of the Java SE Platform.',
#    'tag': 'java.base'}

def get_insert(item):
  buttons = [{"first"  : button[0],
              "second" : button[1]} for button in item["buttons"]]

  return item["tag"], item["summary"], item["detail"], json.dumps(buttons, indent=None)



# ------------------------------------------------------------------------------
def get_inserts(json_items):
  # TODO: Below, I cast out duplicates because the uniqueness constraint must be satisfied. But there should not be duplicates! WTF. --D.S., 30-Apr-2025
  uniques = {}
  for python_item in [get_insert(json_item) for json_item in json_items]:
    tag = python_item[0]
    if tag in uniques:
      print(f"""WARNING: Discarding duplicate '{tag}' item.""")

    else:
      uniques[tag] = python_item

  print(f"Eliminated {len(json_items) - len(uniques)} duplicates.")

  return tuple(uniques.values())



# ------------------------------------------------------------------------------
def report_bad_items(items, keyword, failure_mode):
  print(f"""
{"-" * 80}
WARNING: {len(items)} items were eliminated because the '{keyword}' element is {failure_mode}.
Items missing the '{keyword}' element are:\n""")
  print(f"""{"\n\n".join([pformat(after_item) for after_item in items])}""")



# ------------------------------------------------------------------------------
def main(cursor):
  with open(JSON_FILE) as fd:
    items = json.load(fd)

  print(f"Read {len(items)} JSON entries from '{JSON_FILE}'.")

  inserts = get_inserts(items)

  inserts2  = [insert for insert in inserts if type(insert[2]) == type("")]
  bad_items = [insert for insert in inserts if type(insert[2]) != type("")]
  report_bad_items(bad_items, "detail", "not a string")

  inserts3  = [insert for insert in inserts2 if len(insert[2]) >  0]
  bad_items = [insert for insert in inserts if len(insert[2]) <= 0]
  report_bad_items(bad_items, "detail", "an empty string")
  
  inserts4  = [insert for insert in inserts3 if len(insert[1]) >  0]
  bad_items = [insert for insert in inserts if len(insert[1]) <= 0]
  report_bad_items(bad_items, "summary", "an empty string")

  inserts = inserts4

  cursor.execute("DELETE FROM ide_tooltip_table;") # Delete old content.
  cursor.executemany(INSERT_SQL, inserts)



# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
if __name__ == "__main__":
  with sqlite3.connect(DATABASE_FILENAME) as connection:
    main(connection.cursor())
