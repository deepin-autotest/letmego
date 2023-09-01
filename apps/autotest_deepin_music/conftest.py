"""conftest"""
from os.path import exists
import pytest

from src import logger
from apps.autotest_deepin_music.widget.other_widget import KillDfm
from apps.autotest_deepin_music.widget.deepin_music_widget import DeepinMusicWidget
from apps.autotest_deepin_music.config import Config
from apps.autotest_deepin_music.cleanall import CleanAll


@pytest.fixture(scope="function", autouse=True)
def clean_all(request):
    """clean_all"""
    def clean_music():
        """clean_music"""
        if request.config.getoption("--clean") == "yes":
            logger.debug("Clean All")
            CleanAll.kill_all_process()
            CleanAll.clean_environment()
            DeepinMusicWidget.run_cmd("rm -rf ~/.config/deepin/dde-file-manager.json")
            KillDfm.kill_dfm()
        for i in ["dde-computer.desktop", "dde-trash.desktop"]:
            if not exists(f"/home/{Config.USERNAME}/Desktop/{i}"):
                DeepinMusicWidget.run_cmd(
                    f"cp /usr/share/applications/{i} /home/{Config.USERNAME}/Desktop/",
                    interrupt=False,
                    out_debug_flag=False,
                    command_log=False,
                )

    request.addfinalizer(clean_music)
