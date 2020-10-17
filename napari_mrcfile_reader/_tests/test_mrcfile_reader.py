import numpy as np
import mrcfile
from napari_mrcfile_reader import napari_get_reader


# tmp_path is a pytest fixture
def test_reader(tmp_path):
    # write a fake MRC file using mrcfile
    my_test_file = str(tmp_path / "myfile.mrc")
    original_data = np.random.rand(20, 20).astype(np.float32)
    mrcfile.new(my_test_file, original_data)

    # try to read it back in
    reader = napari_get_reader(my_test_file)
    assert callable(reader)

    # make sure we're delivering the right format
    layer_data_list = reader(my_test_file)
    assert isinstance(layer_data_list, list) and len(layer_data_list) > 0
    layer_data_tuple = layer_data_list[0]
    assert isinstance(layer_data_tuple, tuple) and len(layer_data_tuple) > 0

    # make sure it's the same as it started
    np.testing.assert_allclose(original_data, layer_data_tuple[0])


def test_get_reader_pass():
    reader = napari_get_reader("fake.file")
    assert reader is None
