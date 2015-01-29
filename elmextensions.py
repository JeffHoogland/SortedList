# encoding: utf-8

from efl.elementary.list import List, ELM_LIST_LIMIT, ELM_LIST_COMPRESS
from efl.elementary.label import Label
from efl.elementary.box import Box
from efl.elementary.button import Button
from efl.elementary.scroller import Scroller
from efl.evas import EVAS_HINT_EXPAND, EVAS_HINT_FILL

EXPAND_BOTH = EVAS_HINT_EXPAND, EVAS_HINT_EXPAND
EXPAND_HORIZ = EVAS_HINT_EXPAND, 0.0
FILL_BOTH = EVAS_HINT_FILL, EVAS_HINT_FILL
FILL_HORIZ = EVAS_HINT_FILL, 0.5

#
# TODO ideas:
# - populate with an idler
# - custom cb func for sorting
# - override Table widgets methods
# - move this over to Cython to increase performance if needed
# - custom theme
# - separate title bar?
#

class SortedList(Box):

    """

    A "spread sheet like" widget for elementary.

    Argument "titles" is a list, with each element being a tuple:
    (<Display Text>, <Sortable>)

    """

    def __init__(self, parent_widget, titles=None, initial_sort=0,
        ascending=True, *args, **kwargs):
        Box.__init__(self, parent_widget, *args, **kwargs)

        self.header = titles
        self.sort_column = initial_sort
        self.sort_column_ascending = ascending

        self.rows = []
        self.header_row = []
        self.header_box = Box(self, size_hint_weight=EXPAND_HORIZ,
                size_hint_align=FILL_HORIZ)
        self.header_box.horizontal = True
        self.header_box.show()
        
        scr = Scroller(self, size_hint_weight=EXPAND_BOTH,
                size_hint_align=FILL_BOTH)
        
        self.list_box = Box(self, size_hint_weight=EXPAND_BOTH,
                size_hint_align=FILL_BOTH)
        self.list_box.horizontal = True
        self.list_box.show()
        
        scr.content = self.list_box
        scr.show()
        
        self.lists = []

        self.pack_end(self.header_box)
        self.pack_end(scr)
        self.show()

        if titles is not None:
            self.header_row_pack(titles)

    def header_row_pack(self, titles):

        """Takes a list (or a tuple) of tuples (string, bool) and packs them to
        the first row of the table."""

        assert isinstance(titles, (list, tuple))
        for t in titles:
            assert isinstance(t, tuple)
            assert len(t) == 2
            title, sortable = t
            assert isinstance(title, basestring)
            assert isinstance(sortable, bool)

        def sort_btn_cb(button, col):
            if self.sort_column == col:
                self.reverse()
            else:
                self.sort_by_column(col)

        for count, t in enumerate(titles):
            title, sortable = t
            btn = Button(self, size_hint_weight=EXPAND_HORIZ,
                size_hint_align=FILL_HORIZ, text=title)
            btn.callback_clicked_add(sort_btn_cb, count)
            if not sortable:
                btn.disabled = True
            btn.show()
            self.header_box.pack_end(btn)
            self.header_row.append(btn)
            
            elm_list = List(self, size_hint_weight=EXPAND_BOTH,  size_hint_align=FILL_BOTH)
            print elm_list.Scrollable
            elm_list.go()
            elm_list.show()
            self.list_box.pack_end(elm_list)
            self.lists.append(elm_list)

    def row_pack(self, row, sort=True):

        """Takes a list of items and packs them to the table."""

        assert len(row) == len(self.header_row), (
            "The row you are trying to add to this sorted list has the wrong "
            "number of items! expected: %i got: %i" % (
                len(self.header_row), len(row)
                )
            )

        self.rows.append(row)
        self.add_row(row)

        if sort:
            self.sort_by_column(self.sort_column)
        else:
            self.add_row(row)
    
    def add_row(self, row):
        for count, item in enumerate(row):
            self.lists[count].item_append(str(item))

    def row_unpack(self, row, delete=False):

        """Unpacks and hides, and optionally deletes, a row of items.

        The argument row can either be the row itself or its index number.

        """
        if isinstance(row, int):
            row_index = row
        else:
            row_index = self.rows.index(row)

        # print("row index: " + str(row_index-1))
        # print("length: " + str(len(self.rows)))
        # print("sort_data: " + str(row[self.sort_column].data["sort_data"]))

        row = self.rows.pop(row_index)

        self.sort_by_column(self.sort_column,
            ascending=self.sort_column_ascending)

    def reverse(self):
        self.rows.reverse()
        for our_list in self.lists:
            our_list.clear()
        for row in self.rows:
            self.add_row(row)

        lb = self.header_row[self.sort_column].part_content_get("icon")
        if lb is not None:
            if self.sort_column_ascending:
                lb.text = u"⬆"
                self.sort_column_ascending = False
            else:
                lb.text = u"⬇"
                self.sort_column_ascending = True

    def sort_by_column(self, col, ascending=True):

        assert col >= 0
        assert col < len(self.header_row)

        self.header_row[self.sort_column].icon = None

        btn = self.header_row[col]
        ic = Label(btn)
        btn.part_content_set("icon", ic)
        ic.show()

        if ascending == True: #ascending:
            ic.text = u"⬇"
            self.sort_column_ascending = True
        else:
             ic.text = u"⬆"
             self.sort_column_ascending = False

    
        self.rows.sort(
            key=lambda e: e[col],
            #reverse=False if ascending else True
            )

        if not ascending:
             self.rows.reverse()

        #Clear old data
        for our_list in self.lists:
            our_list.clear()

        for row in self.rows:
            self.add_row(row)

        self.sort_column = col

    def update(self):
        self.sort_by_column(self.sort_column, self.sort_column_ascending)

