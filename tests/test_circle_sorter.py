import unittest

import pandas as pd

from circle_sorter import sort_circle_groups


class SortCircleGroupsTests(unittest.TestCase):
    def test_sorts_circles_and_keeps_items_together(self):
        source = pd.DataFrame([
            {"サークル名": "Circle B", "場所": "10b", "区分": "ア", "地区": "東2", "購入内容": "B item 1"},
            {"サークル名": None, "場所": None, "区分": None, "地区": None, "購入内容": "B item 2"},
            {"サークル名": "Circle C", "場所": "2a", "区分": "イ", "地区": "東1", "購入内容": "C item"},
            {"サークル名": "Circle A", "場所": "2a", "区分": "ア", "地区": "西1", "購入内容": "A item"},
        ])

        result = sort_circle_groups(source)

        self.assertEqual(
            result["購入内容"].tolist(),
            ["A item", "C item", "B item 1", "B item 2"]
        )

    def test_places_blank_location_last(self):
        source = pd.DataFrame([
            {"サークル名": "No location", "場所": None, "区分": None, "地区": None, "購入内容": "unknown"},
            {"サークル名": "Located", "場所": "01a", "区分": "ア", "地区": "東1", "購入内容": "known"},
        ])

        result = sort_circle_groups(source)

        self.assertEqual(
            result["サークル名"].tolist(),
            ["Located", "No location"]
        )


if __name__ == "__main__":
    unittest.main()
