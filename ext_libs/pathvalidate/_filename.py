"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import itertools
import ntpath
import posixpath
import re
from pathlib import Path
from typing import Optional, Pattern, Tuple

from ._base import AbstractSanitizer, BaseFile, BaseValidator
from ._common import (
    PathType,
    Platform,
    PlatformType,
    findall_to_str,
    is_pathlike_obj,
    preprocess,
    validate_pathtype,
)
from .error import ErrorReason, InvalidCharError, InvalidLengthError, ValidationError


_DEFAULT_MAX_FILENAME_LEN = 255
_RE_INVALID_FILENAME = re.compile(
    "[{:s}]".format(re.escape(BaseFile._INVALID_FILENAME_CHARS)), re.UNICODE
)
_RE_INVALID_WIN_FILENAME = re.compile(
    "[{:s}]".format(re.escape(BaseFile._INVALID_WIN_FILENAME_CHARS)), re.UNICODE
)


class FileNameSanitizer(AbstractSanitizer):
    def __init__(
        self,
        min_len: Optional[int] = 1,
        max_len: Optional[int] = _DEFAULT_MAX_FILENAME_LEN,
        platform: PlatformType = None,
        check_reserved: bool = True,
    ) -> None:
        super().__init__(
            min_len=min_len,
            max_len=max_len,
            check_reserved=check_reserved,
            platform_max_len=_DEFAULT_MAX_FILENAME_LEN,
            platform=platform,
        )

        self._sanitize_regexp = self._get_sanitize_regexp()
        self.__validator = FileNameValidator(
            min_len=self.min_len,
            max_len=self.max_len,
            check_reserved=check_reserved,
            platform=self.platform,
        )

    def sanitize(self, value: PathType, replacement_text: str = "") -> PathType:
        try:
            validate_pathtype(value)
        except ValidationError as e:
            if e.reason == ErrorReason.NULL_NAME:
                return ""
            raise

        sanitized_filename = self._sanitize_regexp.sub(replacement_text, str(value))
        sanitized_filename = sanitized_filename[: self.max_len]

        try:
            self.__validator.validate(sanitized_filename)
        except ValidationError as e:
            if e.reason == ErrorReason.RESERVED_NAME and e.reusable_name is False:
                sanitized_filename = re.sub(
                    re.escape(e.reserved_name), "{}_".format(e.reserved_name), sanitized_filename
                )
            elif e.reason == ErrorReason.INVALID_CHARACTER:
                if self.platform in [Platform.UNIVERSAL, Platform.WINDOWS]:
                    sanitized_filename = sanitized_filename.rstrip(" .")

        if is_pathlike_obj(value):
            return Path(sanitized_filename)

        return sanitized_filename

    def _get_sanitize_regexp(self) -> Pattern:
        if self.platform in [Platform.UNIVERSAL, Platform.WINDOWS]:
            return _RE_INVALID_WIN_FILENAME

        return _RE_INVALID_FILENAME


class FileNameValidator(BaseValidator):
    _WINDOWS_RESERVED_FILE_NAMES = ("CON", "PRN", "AUX", "CLOCK$", "NUL") + tuple(
        "{:s}{:d}".format(name, num)
        for name, num in itertools.product(("COM", "LPT"), range(1, 10))
    )
    _MACOS_RESERVED_FILE_NAMES = (":",)

    @property
    def reserved_keywords(self) -> Tuple[str, ...]:
        common_keywords = super().reserved_keywords

        if self._is_universal():
            return (
                common_keywords
                + self._WINDOWS_RESERVED_FILE_NAMES
                + self._MACOS_RESERVED_FILE_NAMES
            )

        if self._is_windows():
            return common_keywords + self._WINDOWS_RESERVED_FILE_NAMES

        if self._is_posix() or self._is_macos():
            return common_keywords + self._MACOS_RESERVED_FILE_NAMES

        return common_keywords

    def __init__(
        self,
        min_len: Optional[int] = 1,
        max_len: Optional[int] = _DEFAULT_MAX_FILENAME_LEN,
        platform: PlatformType = None,
        check_reserved: bool = True,
    ) -> None:
        super().__init__(
            min_len=min_len,
            max_len=max_len,
            check_reserved=check_reserved,
            platform_max_len=_DEFAULT_MAX_FILENAME_LEN,
            platform=platform,
        )

    def validate(self, value: PathType) -> None:
        validate_pathtype(value)

        unicode_filename = preprocess(value)
        value_len = len(unicode_filename)

        self.validate_abspath(unicode_filename)

        if value_len > self.max_len:
            raise InvalidLengthError(
                "filename is too long: expected<={:d}, actual={:d}".format(self.max_len, value_len)
            )
        if value_len < self.min_len:
            raise InvalidLengthError(
                "filename is too short: expected>={:d}, actual={:d}".format(self.min_len, value_len)
            )

        self._validate_reserved_keywords(unicode_filename)

        if self._is_universal() or self._is_windows():
            self.__validate_win_filename(unicode_filename)
        else:
            self.__validate_unix_filename(unicode_filename)

    def validate_abspath(self, value: str) -> None:
        if any([ntpath.isabs(value), posixpath.isabs(value)]):
            raise ValidationError(
                description="found an absolute path ({}), expected a filename".format(value),
                platform=self.platform,
                reason=ErrorReason.FOUND_ABS_PATH,
            )

    def __validate_unix_filename(self, unicode_filename: str) -> None:
        match = _RE_INVALID_FILENAME.findall(unicode_filename)
        if match:
            raise InvalidCharError(
                self._ERROR_MSG_TEMPLATE.format(
                    invalid=findall_to_str(match), value=repr(unicode_filename)
                )
            )

    def __validate_win_filename(self, unicode_filename: str) -> None:
        match = _RE_INVALID_WIN_FILENAME.findall(unicode_filename)
        if match:
            raise InvalidCharError(
                self._ERROR_MSG_TEMPLATE.format(
                    invalid=findall_to_str(match), value=repr(unicode_filename)
                ),
                platform=Platform.WINDOWS,
            )

        if unicode_filename[-1] in (" ", "."):
            raise InvalidCharError(
                self._ERROR_MSG_TEMPLATE.format(
                    invalid=re.escape(unicode_filename[-1]), value=repr(unicode_filename)
                ),
                platform=Platform.WINDOWS,
                description="Do not end a file or directory name with a space or a period",
            )


def validate_filename(
    filename: PathType,
    platform: Optional[str] = None,
    min_len: int = 1,
    max_len: int = _DEFAULT_MAX_FILENAME_LEN,
    check_reserved: bool = True,
) -> None:
    """Verifying whether the ``filename`` is a valid file name or not.

    Args:
        filename:
            Filename to validate.
        platform:
            Target platform name of the filename.

            .. include:: platform.txt
        min_len:
            Minimum length of the ``filename``. The value must be greater or equal to one.
            Defaults to ``1``.
        max_len:
            Maximum length of the ``filename``. The value must be lower than:

                - ``Linux``: 4096
                - ``macOS``: 1024
                - ``Windows``: 260
                - ``universal``: 260

            Defaults to ``255``.
        check_reserved:
            If |True|, check reserved names of the ``platform``.

    Raises:
        ValidationError (ErrorReason.INVALID_LENGTH):
            If the ``filename`` is longer than ``max_len`` characters.
        ValidationError (ErrorReason.INVALID_CHARACTER):
            If the ``filename`` includes invalid character(s) for a filename:
            |invalid_filename_chars|.
            The following characters are also invalid for Windows platform:
            |invalid_win_filename_chars|.
        ValidationError (ErrorReason.RESERVED_NAME):
            If the ``filename`` equals reserved name by OS.
            Windows reserved name is as follows:
            ``"CON"``, ``"PRN"``, ``"AUX"``, ``"NUL"``, ``"COM[1-9]"``, ``"LPT[1-9]"``.

    Example:
        :ref:`example-validate-filename`

    See Also:
        `Naming Files, Paths, and Namespaces - Win32 apps | Microsoft Docs
        <https://docs.microsoft.com/en-us/windows/win32/fileio/naming-a-file>`__
    """

    FileNameValidator(
        platform=platform, min_len=min_len, max_len=max_len, check_reserved=check_reserved
    ).validate(filename)


def is_valid_filename(
    filename: PathType,
    platform: Optional[str] = None,
    min_len: int = 1,
    max_len: Optional[int] = None,
    check_reserved: bool = True,
) -> bool:
    return FileNameValidator(
        platform=platform, min_len=min_len, max_len=max_len, check_reserved=check_reserved
    ).is_valid(filename)


def sanitize_filename(
    filename: PathType,
    replacement_text: str = "",
    platform: Optional[str] = None,
    max_len: Optional[int] = _DEFAULT_MAX_FILENAME_LEN,
    check_reserved: bool = True,
) -> PathType:
    """Make a valid filename from a string.

    To make a valid filename the function does:

        - Replace invalid characters as file names included in the ``filename``
          with the ``replacement_text``. Invalid characters are:

            - unprintable characters
            - |invalid_filename_chars|
            - for Windows (or universal) only: |invalid_win_filename_chars|

        - Append underscore (``"_"``) at the tail of the name if sanitized name
          is one of the reserved names by the operating system
          (only when ``check_reserved`` is |True|).

    Args:
        filename: Filename to sanitize.
        replacement_text:
            Replacement text for invalid characters. Defaults to ``""``.
        platform:
            Target platform name of the filename.

            .. include:: platform.txt
        max_len:
            Maximum length of the ``filename`` length. Truncate the name length if
            the ``filename`` length exceeds this value.
            Defaults to ``255``.
        check_reserved:
            If |True|, sanitize reserved names of the ``platform``.

    Returns:
        Same type as the ``filename`` (str or PathLike object):
            Sanitized filename.

    Raises:
        ValueError:
            If the ``filename`` is an invalid filename.

    Example:
        :ref:`example-sanitize-filename`
    """

    return FileNameSanitizer(
        platform=platform, max_len=max_len, check_reserved=check_reserved
    ).sanitize(filename, replacement_text)
