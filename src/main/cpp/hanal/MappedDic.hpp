/**
 * @author     krikit(krikit@naver.com)
 * @copyright  Copyright (C) 2014-2015, krikit. All rights reserved. BSD 2-Clause License
 */

#ifndef HANAL_MAPPEDDIC_HPP
#define HANAL_MAPPEDDIC_HPP


//////////////
// includes //
//////////////
#include <string>

#include "boost/iostreams/device/mapped_file.hpp"
#include "boost/lexical_cast.hpp"

#include "hanal/Except.hpp"


namespace hanal {


template<typename T>
class MappedDic {
 public:
  virtual ~MappedDic() {
    close();
  }

  /**
   * @brief        open resource file
   * @param  path  file path
   */
  virtual void open(std::string path) {
    close();
    try {
      _source.open(path);
    } catch (std::exception exc) {
      HANAL_THROW(exc.what());
    }
    if (!_source.is_open()) HANAL_THROW("Fail to open file: " + path);
    if ((_source.size() > 0) && ((_source.size() % sizeof(T) != 0))) {
      close();
      HANAL_THROW("Invalid size of file: " + boost::lexical_cast<std::string>(_source.size()));
    }
  }

  /**
   * @brief  close resource file
   */
  virtual void close() {
    _source.close();
  }

  /**
   * @brief  get data pointer
   */
  virtual const T* data() {
    return reinterpret_cast<const T*>(_source.data());
  }

 private:
  boost::iostreams::mapped_file_source _source;    ///< mmap file
};


}    // namespace hanal


#endif  // HANAL_MAPPEDDIC_HPP
