# encoding: utf-8

from efl.evas import EVAS_HINT_EXPAND, EVAS_HINT_FILL
from efl.elementary.box import Box
from efl.elementary.button import Button
from efl.elementary.icon import Icon
from efl.elementary.separator import Separator
from efl.elementary.scroller import Scroller
from efl.elementary.naviframe import Naviframe

EXPAND_BOTH = EVAS_HINT_EXPAND, EVAS_HINT_EXPAND
EXPAND_HORIZ = EVAS_HINT_EXPAND, 0.0
FILL_BOTH = EVAS_HINT_FILL, EVAS_HINT_FILL
FILL_HORIZ = EVAS_HINT_FILL, 0.5
EXPAND_NONE = 0.0, 0.0
ALIGN_CENTER = 0.5, 0.5
ALIGN_RIGHT = 1.0, 0.5
ALIGN_LEFT = 0.0, 0.5

class TabbedBox(Box):
    def __init__(self, parent_widget, *args, **kwargs):
        Box.__init__(self, parent_widget, *args, **kwargs)

        self.tabs = []
        self.currentTab = None

        self.scr = Scroller(self, size_hint_weight=EXPAND_HORIZ,
                           size_hint_align=FILL_BOTH)
        self.scr.content_min_limit(False, True)

        self.buttonBox = Box(self.scr, size_hint_weight=EXPAND_HORIZ,
                           size_hint_align=ALIGN_LEFT)
        self.buttonBox.horizontal = True
        self.buttonBox.show()

        self.scr.content = self.buttonBox
        self.scr.show()
        
        self.nf = Naviframe(self, size_hint_weight=EXPAND_BOTH,
                               size_hint_align=FILL_BOTH)
        self.nf.show()

        self.pack_end(self.scr)
        self.pack_end(self.nf)
        
    def addTab(self, widget, tabName, canClose=True):
        self.tabs.append(widget)

        btn = Button(self.buttonBox, style="anchor", size_hint_align=ALIGN_LEFT)
        btn.text = tabName
        btn.data["widget"] = widget
        btn.callback_clicked_add(self.showTab, widget)
        btn.show()

        icn = Icon(self.buttonBox)
        icn.standard_set("gtk-close")
        icn.show()

        cls = Button(self.buttonBox, content=icn, style="anchor", size_hint_align=ALIGN_LEFT)
        cls.data["widget"] = widget
        cls.callback_clicked_add(self.closeTab)
        if canClose:
            cls.show()

        sep = Separator(self.buttonBox, size_hint_align=ALIGN_LEFT)
        sep.show()

        self.buttonBox.pack_end(btn)
        self.buttonBox.pack_end(cls)
        self.buttonBox.pack_end(sep)

        #Arguments go: btn, cls, sep
        widget.data["close"] = cls
        widget.data["button"] = btn
        widget.data["sep"] = sep
        
        self.showTab(widget=widget)
    
    def showTab(self, btn=None, widget=None):
        if self.currentTab:
            self.currentTab.data["button"].style="anchor"
        self.nf.item_simple_push(widget)
        self.currentTab = widget
        self.currentTab.data["button"].style="widget"
    
    def closeTab(self, btn):
        del self.tabs[self.tabs.index(btn.data["widget"])]
        
        self.buttonBox.unpack(btn.data["widget"].data["close"])
        self.buttonBox.unpack(btn.data["widget"].data["button"])
        self.buttonBox.unpack(btn.data["widget"].data["sep"])
        
        btn.data["widget"].data["close"].delete()
        btn.data["widget"].data["button"].delete()
        btn.data["widget"].data["sep"].delete()
        btn.data["widget"].delete()
        
        if self.currentTab == btn.data["widget"] and len(self.tabs):
            self.showTab(widget=self.tabs[0])