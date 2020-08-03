# coding=utf-8
# Use pathlib instead of os.path
from pathlib import Path
import logging

try:
    from qgis.core import QgsStyleV2 as QgsStyle
except ImportError:
    from qgis.core import QgsStyle

from resource_sharing.resource_handler.base import BaseResourceHandler
from resource_sharing.symbol_xml_extractor import SymbolXMLExtractor
from resource_sharing.resource_handler.symbol_resolver_mixin import \
    SymbolResolverMixin
from resource_sharing.utilities import qgis_version

LOGGER = logging.getLogger('QGIS Resource Sharing')
SYMBOL = 'symbol'


class SymbolResourceHandler(BaseResourceHandler, SymbolResolverMixin):
    """Concrete class of the Symbol handler."""
    IS_DISABLED = False

    def __init__(self, collection_id):
        """Constructor of the base class."""
        BaseResourceHandler.__init__(self, collection_id)
        # Initialize with the default style
        self.style = QgsStyle.defaultStyle()

    @classmethod
    def dir_name(self):
        return SYMBOL

    def _get_parent_group_or_tag(self):
        """Retrieve or create the parent group (for QGIS2)
        or parent tag (for QGIS3) for the styles.
        Returns the id of the (existing or new) group or tag."""
        parent_group_name = '%s (%s)' % (
            self.collection['name'], self.collection['repository_name'])
        try:
            # QGIS 2
            group = self.style.groupId(parent_group_name)
            if group != 0:
                return group
            return self.style.addGroup(parent_group_name)
        except AttributeError:
            # # not QGIS 2, so hopefully QGIS 3
            # tag = self.style.tagId(parent_group_name)
            # if tag != 0:
            #     return tag
            # return self.style.addTag(parent_group_name)
            # # We don't want to create an empty "parent" tag
            return None

    def _get_child_group_tag(self, group_or_tag_id, file_name):
        """Retrieve or create the child group (for QGIS2) or the tag
        (QGIS3, no hierarchy) for the styles.
        Returns the id of the group or tag id.
        Use a slash and the file_name as a way of simulating a tree
        in QGIS3.
        """
        try:
            # QGIS 2
            group = self.style.groupId(file_name)
            if group != 0:
                return group
            return self.style.addGroup(file_name, group_or_tag_id)
        except AttributeError:
            # not QGIS 2, so hopefully QGIS 3
            # tag_name = self.style.tag(group_or_tag_id) + '/' + file_name
            tag_name = ('%s (%s)/') % (self.collection['name'],
                                       self.collection['repository_name']) + file_name
            tag = self.style.tagId(tag_name)
            if tag != 0:
                return tag
            return self.style.addTag(tag_name)

    def _get_child_groups_tags_ids(self):
        """Retrieve ids for the child groups (for QGIS2) or tags
           (for QGIS3)."""
        parent_group_name = '%s (%s)' % (
            self.collection['name'], self.collection['repository_name'])
        try:
            # QGIS 2
            return [self.style.groupId(n) for n in
                    self.style.childGroupNames(parent_group_name)]
        except AttributeError:
            # not QGIS 2, so hopefully QGIS 3
            return [self.style.tagId(tag) for tag in self.style.tags()
                    if tag.find(parent_group_name) == 0]

    def _get_symbols_for_group_or_tag(self, symbol_type,
                                      child_group_or_tag_id):
        """Return all the symbols for the given group (QGIS2) or tag
        (QGIS3) id."""
        try:
            # QGIS 2
            return self.style.symbolsOfGroup(
                symbol_type, child_group_or_tag_id)
        except AttributeError:
            # not QGIS 2, so hopefully QGIS 3
            return self.style.symbolsWithTag(
                symbol_type, child_group_or_tag_id)

    def _group_or_tag(self, symbol_type, symbol_name, tag_or_group):
        """Add the symbol to a group (QGIS2) or tag the symbol (QGIS3)."""
        try:
            # QGIS 2
            self.style.group(symbol_type, symbol_name, tag_or_group)
        except AttributeError:
            # not QGIS 2, so hopefully QGIS 3
            self.style.tagSymbol(symbol_type, symbol_name,
                                 [self.style.tag(tag_or_group)])

    def _group_or_tag_remove(self, group_or_tag_id):
        """Remove a group (QGIS 2) or tag (QGIS 3)."""
        try:
            # QGIS 2
            self.style.remove(QgsStyle.GroupEntity, group_or_tag_id)
        except AttributeError:
            # not QGIS 2, so hopefully QGIS 3
            if group_or_tag_id is not None:
                self.style.remove(QgsStyle.TagEntity, group_or_tag_id)

    def install(self):
        """Install the symbols from this collection in the QGIS default style.

        For QGIS 2, a group with the name of the collection is created,
        and for each of the XML files in the collection, a child group
        is created, where the symbols and colorramps defined in the XML
        file are stored.
        For QGIS 3, for each of the XML files in the collection, a tag
        is created, and the tag is used for the symbols and colorramps
        defined in that XML file.
        """
        # Skip installation if the directory does not exist
        if not Path(self.resource_dir).exists():
            return
        # Uninstall first (in case it is a reinstall)
        self.uninstall()
        # Get all the symbol XML files in the collection
        symbol_files = []
        valid = 0
        for item in Path(self.resource_dir).glob('*.xml'):
            symbol_files.append(item)
            valid += 1
        # If there are no symbol files, there is nothing to do
        if len(symbol_files) == 0:
            return
        # Only relevant for QGIS 2!
        group_or_tag_id = self._get_parent_group_or_tag()
        for symbol_file in symbol_files:
            file_name = symbol_file.stem
            # Groups in QGIS2, tags in QGIS3...
            groupOrTag_id = self._get_child_group_tag(group_or_tag_id,
                                                      file_name)
            # Modify the symbol file to fix image and SVG paths
            self.resolve_dependency(str(symbol_file))
            # Add all symbols and colorramps and group / tag them
            symbol_xml_extractor = SymbolXMLExtractor(str(symbol_file))
            for symbol in symbol_xml_extractor.symbols:
                symbol_name = '%s (%s)' % (symbol['name'],
                                           self.collection['repository_name'])
                # self.resolve_dependency(symbol[SYMBOL])
                if self.style.addSymbol(symbol_name, symbol[SYMBOL], True):
                    self._group_or_tag(QgsStyle.SymbolEntity, symbol_name,
                                       groupOrTag_id)
            for colorramp in symbol_xml_extractor.colorramps:
                colorramp_name = '%s (%s)' % (
                    colorramp['name'], self.collection['repository_name'])
                if self.style.addColorRamp(
                        colorramp_name, colorramp['colorramp'], True):
                    self._group_or_tag(QgsStyle.ColorrampEntity,
                                       colorramp_name, groupOrTag_id)
            # textformat and labelsettings were introduced in QGIS 3.10
            if qgis_version() < 31000:
                continue
            for textformat in symbol_xml_extractor.textformats:
                textformat_name = '%s (%s)' % (
                    textformat['name'], self.collection['repository_name'])
                if self.style.addTextFormat(
                        textformat_name, textformat['textformat'], True):
                    self._group_or_tag(QgsStyle.TextFormatEntity,
                                       textformat_name, groupOrTag_id)
            for labelsetting in symbol_xml_extractor.labelsettings:
                labelsetting_name = '%s (%s)' % (
                    labelsetting['name'], self.collection['repository_name'])
                if self.style.addLabelSettings(labelsetting_name,
                                               labelsetting['labelsettings'],
                                               True):
                    self._group_or_tag(QgsStyle.LabelSettingsEntity,
                                       labelsetting_name, groupOrTag_id)
        if valid >= 0:
            self.collection[SYMBOL] = valid

    def uninstall(self):
        """Uninstall the symbols from QGIS."""
        # Get the parent group id (not relevant for QGIS 3)
        group_or_tag_id = self._get_parent_group_or_tag()
        # Get the ids of the groups / tags that contain symbols
        child_groups_or_tags_ids = self._get_child_groups_tags_ids()
        for child_group_id in child_groups_or_tags_ids:
            # Get all the symbols from this tag / child group and remove them
            symbols = self._get_symbols_for_group_or_tag(
                QgsStyle.SymbolEntity, child_group_id)
            for symbol in symbols:
                self.style.removeSymbol(symbol)
            # Get all the colorramps for this tag / child group and remove them
            colorramps = self._get_symbols_for_group_or_tag(
                QgsStyle.ColorrampEntity, child_group_id)
            for colorramp in colorramps:
                self.style.removeColorRamp(colorramp)
            # textformat and labelsettings were introduced in QGIS 3.10
            if qgis_version() < 31000:
                # Remove this tag / child group
                self._group_or_tag_remove(child_group_id)
                continue
            # Get all the textformats for this tag / child group
            # and remove them
            textformats = self._get_symbols_for_group_or_tag(
                QgsStyle.TextFormatEntity, child_group_id)
            for textformat in textformats:
                self.style.removeTextFormat(textformat)
            # Get all the labelsettings for this tag / child group
            # and remove them
            labelsettings = self._get_symbols_for_group_or_tag(
                QgsStyle.LabelSettingsEntity, child_group_id)
            for labelsetting in labelsettings:
                self.style.removeLabelSettings(labelsetting)
            # Remove this tag / child group
            self._group_or_tag_remove(child_group_id)
        # Remove the group / tag:
        self._group_or_tag_remove(group_or_tag_id)
