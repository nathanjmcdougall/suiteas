from pathlib import Path

from suiteas.domain import Class, Codebase, File, Func, ProjConfig
from suiteas.read.codebase import get_codebase


class TestGetCodebase:
    def test_trivial_pass(self, projs_parent_dir: Path) -> None:
        proj_dir = projs_parent_dir / "trivial_pass"
        config = ProjConfig(pkg_names=["af8o7tt1"])
        pkg_dir = proj_dir / config.src_rel_path / "af8o7tt1"

        codebase = get_codebase(proj_dir=proj_dir, config=config)

        assert codebase == Codebase(
            files=[
                File(
                    path=pkg_dir / "__init__.py",
                    funcs=[],
                    clses=[],
                    imported_objs=[],
                ),
            ],
        )

    def test_one_func_no_test(self, projs_parent_dir: Path) -> None:
        proj_dir = projs_parent_dir / "one_func_no_test"
        config = ProjConfig(pkg_names=["pp8cadfs"])
        pkg_dir = proj_dir / config.src_rel_path / "pp8cadfs"

        codebase = get_codebase(proj_dir=proj_dir, config=config)

        assert codebase == Codebase(
            files=[
                File(
                    path=pkg_dir / "__init__.py",
                    funcs=[
                        Func(
                            name="hello",
                            full_name="pp8cadfs.hello",
                            line_num=1,
                            char_offset=0,
                        ),
                    ],
                    clses=[],
                    imported_objs=[],
                ),
            ],
        )

    def test_two_files(self, projs_parent_dir: Path) -> None:
        proj_dir = projs_parent_dir / "two_files"
        config = ProjConfig(pkg_names=["ow9xem9x"])
        pkg_dir = proj_dir / config.src_rel_path / "ow9xem9x"

        codebase = get_codebase(proj_dir=proj_dir, config=config)

        assert codebase == Codebase(
            files=[
                File(
                    path=pkg_dir / "__init__.py",
                    funcs=[],
                    clses=[],
                    imported_objs=[],
                ),
                File(
                    path=pkg_dir / "goodbye.py",
                    funcs=[
                        Func(
                            name="goodbye",
                            full_name="ow9xem9x.goodbye.goodbye",
                            line_num=1,
                            char_offset=0,
                        ),
                    ],
                    clses=[
                        Class(
                            name="Banana",
                            full_name="ow9xem9x.goodbye.Banana",
                            line_num=4,
                            char_offset=0,
                            has_funcs=False,
                        ),
                    ],
                    imported_objs=[],
                ),
                File(
                    path=pkg_dir / "hello.py",
                    funcs=[
                        Func(
                            name="hello",
                            full_name="ow9xem9x.hello.hello",
                            line_num=1,
                            char_offset=0,
                        ),
                    ],
                    clses=[],
                    imported_objs=[],
                ),
            ],
        )
