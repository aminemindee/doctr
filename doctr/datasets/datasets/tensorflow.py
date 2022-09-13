# Copyright (C) 2021-2022, Mindee.

# This program is licensed under the Apache License 2.0.
# See LICENSE or go to <https://opensource.org/licenses/Apache-2.0> for full license details.

import os
from copy import deepcopy
from typing import Any, List, Tuple

import numpy as np
import tensorflow as tf

from doctr.io import read_img_as_tensor, tensor_from_numpy

from .base import _AbstractDataset, _VisionDataset

__all__ = ["AbstractDataset", "VisionDataset"]


class AbstractDataset(_AbstractDataset):
    def _read_sample(self, index: int) -> Tuple[tf.Tensor, Any]:
        img_name, target = self.data[index]

        # Check target
        if isinstance(target, dict):
            assert "boxes" in target, "Target should contain 'boxes' key"
            assert "labels" in target, "Target should contain 'labels' key"
        elif isinstance(target, tuple):
            assert isinstance(target[0], str) or isinstance(
                target[0], np.ndarray
            ), "Target should be a string or a numpy array"
        else:
            assert isinstance(target, str) or isinstance(
                target, np.ndarray
            ), "Target should be a string or a numpy array"

        # Read image
        img = (
            tensor_from_numpy(img_name, dtype=tf.float32)
            if isinstance(img_name, np.ndarray)
            else read_img_as_tensor(os.path.join(self.root, img_name), dtype=tf.float32)
        )

        return img, deepcopy(target)

    @staticmethod
    def collate_fn(samples: List[Tuple[tf.Tensor, Any]]) -> Tuple[tf.Tensor, List[Any]]:

        images, targets = zip(*samples)
        images = tf.stack(images, axis=0)

        return images, list(targets)


class VisionDataset(AbstractDataset, _VisionDataset):
    pass
