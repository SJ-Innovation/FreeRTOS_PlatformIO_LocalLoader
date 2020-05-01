from glob import glob
from os import listdir, remove
from os.path import basename, isdir, isfile, join, dirname, realpath
from shutil import copy
from string import Template
import sys
from pathlib import Path

from SCons.Script import DefaultEnvironment

from platformio import util
from platformio.builder.tools.piolib import PlatformIOLibBuilder

env = DefaultEnvironment()
platform = env.PioPlatform()
board = env.BoardConfig()

THIS_SCRIPT_DIR = Path().absolute()

FREERTOS_FIRMWARE_DIR = None  ## "Or a path here"
if FREERTOS_FIRMWARE_DIR is None:
    FREERTOS_FW_NAME = None  ## "Or a name here"
    if FREERTOS_FW_NAME is None:
        for i in listdir(THIS_SCRIPT_DIR):
            if "FreeRTOS_" in i:
                FREERTOS_FW_NAME = i
                break
    assert FREERTOS_FW_NAME is not None
    FREERTOS_FIRMWARE_DIR = join(THIS_SCRIPT_DIR, FREERTOS_FW_NAME)
assert isdir(FREERTOS_FIRMWARE_DIR)


class CustomLibBuilder(PlatformIOLibBuilder):
    PARSE_SRC_BY_H_NAME = False

    # Max depth of nested includes:
    # -1 = unlimited
    # 0 - disabled nesting
    # >0 - number of allowed nested includes
    CCONDITIONAL_SCANNER_DEPTH = 0

    # For cases when sources located not only in "src" dir
    @property
    def src_dir(self):
        return self.path


env.Append(
    CPPPATH=[
        join(FREERTOS_FIRMWARE_DIR, "FreeRTOS", "Source", "include")
    ]
)

libs = []

libs.append(env.BuildLibrary(
    join("$BUILD_DIR", "FreeRTOS"),
    join(FREERTOS_FIRMWARE_DIR, "FreeRTOS", "Source"),
    src_filter="+<*> -<portable/*> +<portable/GCC/ARM_CM7/*>"
))
