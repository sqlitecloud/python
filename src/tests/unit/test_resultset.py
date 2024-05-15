import pytest
from sqlitecloud.resultset import SQCloudResult, SqliteCloudResultSet


class TestSqCloudResult:
    def test_init_data(self):
        result = SQCloudResult()
        result.init_data(42)
        assert 1 == result.nrows
        assert 1 == result.ncols
        assert [42] == result.data
        assert True is result.is_result

    # TODO
    def test_init_data_with_array(self):
        result = SQCloudResult()
        result.init_data([42, 43, 44])
        assert 1 == result.nrows
        assert 1 == result.ncols
        assert [42, 43, 44] == result.data
        assert True is result.is_result

    def test_init_as_dataset(self):
        result = SQCloudResult()
        assert False is result.is_result
        assert 0 == result.nrows
        assert 0 == result.ncols
        assert 0 == result.version


class TestSqliteCloudResultSet:
    def test_next(self):
        result = SQCloudResult(result=42)
        result_set = SqliteCloudResultSet(result)

        assert {"result": 42} == next(result_set)
        with pytest.raises(StopIteration):
            next(result_set)

    def test_iter_result(self):
        result = SQCloudResult(result=42)
        result_set = SqliteCloudResultSet(result)
        for row in result_set:
            assert {"result": 42} == row

    def test_iter_rowset(self):
        rowset = SQCloudResult()
        rowset.nrows = 2
        rowset.ncols = 2
        rowset.colname = ["name", "age"]
        rowset.data = ["John", 42, "Doe", 24]
        rowset.version = 2
        result_set = SqliteCloudResultSet(rowset)

        out = []
        for row in result_set:
            out.append(row)

        assert 2 == len(out)
        assert {"name": "John", "age": 42} == out[0]
        assert {"name": "Doe", "age": 24} == out[1]

    def test_get_value_with_rowset(self):
        rowset = SQCloudResult()
        rowset.nrows = 2
        rowset.ncols = 2
        rowset.colname = ["name", "age"]
        rowset.data = ["John", 42, "Doe", 24]
        rowset.version = 2
        result_set = SqliteCloudResultSet(rowset)

        assert "John" == result_set.get_value(0, 0)
        assert 24 == result_set.get_value(1, 1)
        assert None == result_set.get_value(2, 2)

    def test_get_value_array(self):
        result = SQCloudResult(result=[1, 2, 3, 4, 5, 6])
        result_set = SqliteCloudResultSet(result)
        assert 1 == result_set.get_value(0, 0)
        assert 5 == result_set.get_value(1, 2)
        assert 4 == result_set.get_value(2, 1)
        assert None == result_set.get_value(3, 3)

    def test_get_colname(self):
        result = SQCloudResult()
        result.ncols = 2
        result.colname = ["name", "age"]
        result_set = SqliteCloudResultSet(result)
        assert "name" == result_set.get_name(0)
        assert "age" == result_set.get_name(1)
        assert None == result_set.get_name(2)