from __future__ import absolute_import, division, print_function

import pytest

from qtpy.QtCore import Qt
from glue.core import Data, DataCollection, Session

from ..viewer_widget import DataTableModel, TableWidget


class TestDataTableModel():

    def setup_method(self, method):
        self.data = Data(x=[1, 2, 3, 4], y=[2, 3, 4, 5])
        self.model = DataTableModel(self.data)

    def test_column_count(self):
        assert self.model.columnCount() == 2

    def test_column_count_hidden(self):
        self.model.show_hidden = True
        assert self.model.columnCount() == 4

    def test_header_data(self):
        for i, c in enumerate(self.data.visible_components):
            result = self.model.headerData(i, Qt.Horizontal, Qt.DisplayRole)
            assert result == c.label

        for i in range(self.data.size):
            result = self.model.headerData(i, Qt.Vertical, Qt.DisplayRole)
            assert result == str(i)

    def test_row_count(self):
        assert self.model.rowCount() == 4

    def test_data(self):
        for i, c in enumerate(self.data.visible_components):
            for j in range(self.data.size):
                idx = self.model.index(j, i)
                result = self.model.data(idx, Qt.DisplayRole)
                assert float(result) == self.data[c, j]

    @pytest.mark.xfail
    def test_data_2d(self):
        self.data = Data(x=[[1, 2], [3, 4]], y=[[2, 3], [4, 5]])
        self.model = DataTableModel(self.data)
        for i, c in enumerate(self.data.visible_components):
            for j in range(self.data.size):
                idx = self.model.index(j, i)
                result = self.model.data(idx, Qt.DisplayRole)
                assert float(result) == self.data[c].ravel()[j]


def test_table_widget():

    d = Data(a=[1,2,3,4,5], b=[1.2, 3.3, 4.5, 3.2, 2.2], c=['a','b','c','d','e'])
    dc = DataCollection([d])
    session = Session(dc, hub=dc.hub)

    widget = TableWidget(session)
    widget.add_data(d)
    widget.show()
