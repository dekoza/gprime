# -*- coding: utf-8 -*-
#
# Gramps - a GTK+/GNOME based genealogy program
#
# Copyright (C) 2004-2006  Donald N. Allingham
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

#-------------------------------------------------------------------------
#
# Python modules
#
#-------------------------------------------------------------------------

"""
Traditional-Chinese-specific classes for parsing and displaying dates.
"""
from __future__ import unicode_literals
import re

#-------------------------------------------------------------------------
#
# GRAMPS modules
#
#-------------------------------------------------------------------------

from ..lib.date import Date
from ._dateparser import DateParser
from ._datedisplay import DateDisplay
from ._datehandler import register_datehandler

#-------------------------------------------------------------------------
#
# Traditional-Chinese parser
#
#-------------------------------------------------------------------------
class DateParserZH_TW(DateParser):
    """
    Convert a text string into a Date object. If the date cannot be
    converted, the text string is assigned.
    """
    
    # modifiers before the date
    modifier_to_int = {
        '以前'   : Date.MOD_BEFORE,
        '以後'   : Date.MOD_AFTER,
        '大約'   : Date.MOD_ABOUT,
        }

    month_to_int = DateParser.month_to_int

    month_to_int["正"] = 1
    month_to_int["一"] = 1
    month_to_int["zhēngyuè"] = 1
    month_to_int["二"] = 2
    month_to_int["èryuè"] = 2
    month_to_int["三"] = 3
    month_to_int["sānyuè"] = 3
    month_to_int["四"] = 4
    month_to_int["sìyuè"] = 4
    month_to_int["五"] = 5
    month_to_int["wǔyuè"] = 5
    month_to_int["六"] = 6
    month_to_int["liùyuè"] = 6
    month_to_int["七"] = 7
    month_to_int["qīyuè"] = 7
    month_to_int["八"] = 8
    month_to_int["bāyuè"] = 8
    month_to_int["九"] = 9
    month_to_int["jiǔyuè"] = 9
    month_to_int["十"] = 10
    month_to_int["shíyuè"] = 10
    month_to_int["十一"] = 11
    month_to_int["shíyīyuè"] = 11
    month_to_int["十二"] = 12
    month_to_int["shí'èryuè"] = 12
    month_to_int["假閏"] = 13
    month_to_int["jiǎ rùn yùe"] = 13
    
    calendar_to_int = {
        '陽曆'             : Date.CAL_GREGORIAN,
        'g'                : Date.CAL_GREGORIAN,
        '儒略曆'           : Date.CAL_JULIAN,
        'j'                : Date.CAL_JULIAN,
        '希伯來歷'         : Date.CAL_HEBREW,
        'h'                : Date.CAL_HEBREW,
        '伊斯蘭曆'         : Date.CAL_ISLAMIC,
        'i'                : Date.CAL_ISLAMIC,
        '法國共和歷'       : Date.CAL_FRENCH,
        'f'                : Date.CAL_FRENCH,
        '伊郎歷'           : Date.CAL_PERSIAN,
        'p'                : Date.CAL_PERSIAN, 
        '瑞典歷'           : Date.CAL_SWEDISH,
        's'                : Date.CAL_SWEDISH,
        }
        
    quality_to_int = {
        '據估計'     : Date.QUAL_ESTIMATED,
        '據計算'     : Date.QUAL_CALCULATED,
        }
        
    # FIXME translate these English strings into traditional-Chinese ones
    bce = ["before calendar", "negative year"] + DateParser.bce

    def init_strings(self):
        """
        This method compiles regular expression strings for matching dates.
        """
        DateParser.init_strings(self)
        _span_1 = ['自']
        _span_2 = ['至']
        _range_1 = ['介於']
        _range_2 = ['與']
        self._span =  re.compile("(%s)\s+(?P<start>.+)\s+(%s)\s+(?P<stop>.+)" %
                                 ('|'.join(_span_1), '|'.join(_span_2)),
                                 re.IGNORECASE)
        self._range = re.compile("(%s)\s+(?P<start>.+)\s+(%s)\s+(?P<stop>.+)" %
                                 ('|'.join(_range_1), '|'.join(_range_2)),
                                 re.IGNORECASE)
                                    
#-------------------------------------------------------------------------
#
# Traditional-Chinese display
#
#-------------------------------------------------------------------------
class DateDisplayZH_TW(DateDisplay):
    """
    Traditional-Chinese language date display class. 
    """

    # this is used to display the 12 gregorian months
    long_months = ( "", "正月", "二月", "三月", "四月", "五月", 
                    "六月", "七月", "八月", "九月", "十月", 
                    "十一月", "十二月" )
    
    short_months = ( "", "一月", "二月", "三月", "四月", "五月", "六月",
                     "七月", "八月", "九月", "十月", "十一月", "十二月" )

    formats = (
        "年年年年-月月-日日 (ISO)", "數字格式", "月 日，年", 
        "月 日，年", "日 月 年",  "日 月 年"
        )
        # this must agree with DateDisplayEn's "formats" definition
        # (since no locale-specific _display_gregorian exists, here)
    
    calendar = (
        "", "儒略曆", "希伯來歷", "法國共和歷", 
        "伊郎歷", "伊斯蘭曆", "瑞典歷" 
        )

    _mod_str = ("", "以前 ", "以後 ", "大約 ", "", "", "")

    _qual_str = ("", "據估計 ", "據計算 ", "")

    # FIXME translate these English strings into traditional-Chinese ones
    _bce_str = "%s B.C.E."


    def display(self, date):
        """
        Return a text string representing the date.
        """
        mod = date.get_modifier()
        cal = date.get_calendar()
        qual = date.get_quality()
        start = date.get_start_date()
        newyear = date.get_new_year()

        qual_str = (self._qual_str)[qual]

        if mod == Date.MOD_TEXTONLY:
            return date.get_text()
        elif start == Date.EMPTY:
            return ""
        elif mod == Date.MOD_SPAN:
            d1 = self.display_cal[cal](start)
            d2 = self.display_cal[cal](date.get_stop_date())
            scal = self.format_extras(cal, newyear)
            return "%s%s %s %s %s%s" % (qual_str, '自', d1, '至', d2, scal)
        elif mod == Date.MOD_RANGE:
            d1 = self.display_cal[cal](start)
            d2 = self.display_cal[cal](date.get_stop_date())
            scal = self.format_extras(cal, newyear)
            return "%s%s %s %s %s%s之間" % (qual_str, '介於', d1, '與',
                                        d2, scal)
        else:
            text = self.display_cal[date.get_calendar()](start)
            scal = self.format_extras(cal, newyear)
            return "%s%s%s%s" % (qual_str, (self._mod_str)[mod], text, 
            scal)

#-------------------------------------------------------------------------
#
# Register classes
#
#-------------------------------------------------------------------------

register_datehandler(('zh_TW', 'zh_HK'), 
                     DateParserZH_TW, DateDisplayZH_TW)
