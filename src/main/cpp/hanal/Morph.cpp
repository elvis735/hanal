/**
 * @author     krikit(krikit@naver.com)
 * @copyright  Copyright (C) 2014-2015, krikit. All rights reserved. BSD 2-Clause License
 */


#include "hanal/Morph.hpp"


//////////////
// includes //
//////////////
#include <cwchar>
#include <vector>

#include "hanal/Except.hpp"
#include "hanal/Util.hpp"


namespace hanal {


////////////////////
// ctors and dtor //
////////////////////
Morph::Morph(const wchar_t* lex_, SejongTag tag_) : lex(lex_), tag(tag_) {
}


/////////////
// methods //
/////////////
SHDPTR(Morph) Morph::parse(wchar_t* morph_str) {
  wchar_t* found = wcsrchr(morph_str, L'/');
  HANAL_ASSERT(found != nullptr, "Invalid morpheme format: " + Util::to_utf8(morph_str));
  *found = L'\0';
  return std::make_shared<Morph>(morph_str, Util::to_sejong(found + 1));
}


SHDPTRVEC(Morph) Morph::parse_anal_result(wchar_t* morphs_str) {
  static const wchar_t _DELIM = L'\2';    // inter morpheme delimiter
  SHDPTRVEC(Morph) anal_result;
  wchar_t* start = morphs_str;
  for (wchar_t* found = wcschr(morphs_str, _DELIM); found != nullptr; found = wcschr(start, _DELIM)) {
    *found = L'\0';
    anal_result.emplace_back(parse(start));
    start = found + 1;
  }
  anal_result.emplace_back(parse(start));
  return anal_result;
}


std::vector<SHDPTRVEC(Morph)> Morph::parse_anal_result_vec(wchar_t* anal_results_str) {
  static const wchar_t _DELIM = L'\1';    // inter analysis results delimiter
  std::vector<SHDPTRVEC(Morph)> anal_results;
  wchar_t* start = anal_results_str;
  for (wchar_t* found = wcschr(anal_results_str, _DELIM); found != nullptr; found = wcschr(start, _DELIM)) {
    *found = L'\0';
    anal_results.emplace_back(parse_anal_result(start));
    start = found + 1;
  }
  anal_results.emplace_back(parse_anal_result(start));
  return anal_results;
}


}    // namespace hanal
