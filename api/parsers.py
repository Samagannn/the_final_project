from rest_framework.parsers import MultiPartParser
import re
from pprint import pprint


def safe_list_get(l, idx, default=None):
    try:
        return l[idx]
    except IndexError:
        return default




class NestedMultiPartParser(MultiPartParser):

    def parse(self, stream, media_type=None, parser_context=None):
        result = super().parse(stream, media_type, parser_context)
        data = {}
        files = {}

        for key, value in result.data.items():
            self._deep_set(data, key, value)

        for key, value in result.files.items():
            self._deep_set(files, key, value)

        return self.merge_data_files(data, files)

    def _deep_set(self, data, key, value):

        keys = self._parse_keys(key)
        d = data
        for part in keys:
            part_idx = keys.index(part)
            if part.isdigit():
                part = int(part)
                val = safe_list_get(d, part, None)
            else:
                val = d.get(part, None)

            if val is None:
                next_val = safe_list_get(keys, part_idx + 1)

                if next_val is not None:
                    if isinstance(d, list):
                        d.append([] if next_val.isdigit() else {})
                    else:
                        d[part] = [] if next_val.isdigit() else {}
                else:
                    if isinstance(d, list):
                        d.append(value)
                    else:
                        d[part] = value

            d = d[part]

    @staticmethod
    def _parse_keys(key):
        return re.split(r'\[|\]\[|\]', key.strip('[]'))

    @staticmethod
    def merge_data_files(data, files):
        for key, value in files.items():
            if key in data:
                if isinstance(data[key], list):
                    data[key].append(value)
                elif isinstance(data[key], dict):
                    data[key].update(value)
                else:
                    data[key] = [data[key], value]
            else:
                data[key] = value

        return data