import os, infra_lib

configs = infra_lib.Object();
configs.package = "quick-1.0.0"
configs.prod_cc_flags = " -Wno-unused-function  -Wno-unused-parameter -Wno-unused-local-typedefs -Werror ";
configs.global_include_dir = ["include"];
configs.active_remote_branch = "master";
toolchain_path = configs.toolchain_path = os.path.join(os.environ["HOME"], "toolchain");

br = infra_lib.BuildRule();
configs.dependency_configs = [

  br.CppLibrary(
      "toolchain/gtest",
      srcs = [ toolchain_path + "/googletest-release-1.8.1/googletest/src/gtest-all.cc" ],
      global_include_dir = [ toolchain_path + "/googletest-release-1.8.1/googletest/include" ],
      local_include_dir = [ toolchain_path+ "/googletest-release-1.8.1/googletest" ],
      global_link_flags = "-lpthread"),

  br.CppLibrary("toolchain/json11",
                      srcs = [toolchain_path + "/json11-master/json/json11.cpp"],
                      global_include_dir = [ toolchain_path + "/json11-master"]),

  br.CppTest("src/stl_utils_test",
             srcs = ["src/stl_utils_test.cpp"],
             deps = ["tests/test_main",
                     "src/stl_utils"]),

  br.CppLibrary("src/stl_utils",
                hdrs = ["include/quick/stl_utils.hpp"]),

  br.CppTest("src/debug_test",
             srcs = ["src/debug_test.cpp"],
             deps = ["tests/test_main",
                     "src/debug"]),

  br.CppLibrary("src/debug",
                hdrs = ["include/quick/debug.hpp"]),

  br.CppLibrary("src/file_utils",
                hdrs = ["include/quick/file_utils.hpp"],
                srcs = ["src/file_utils.cpp"]),

  br.CppTest("src/file_utils_test",
                srcs = ["src/file_utils_test.cpp"],
                deps = ["src/file_utils"]),

];


configs["CCFLAGS"] = "--std=c++14 -O0 -Wall -Wextra -Wno-sign-compare -fno-omit-frame-pointer -Wnon-virtual-dtor -mpopcnt -msse4.2 -g3 -Woverloaded-virtual -Wno-char-subscripts -Werror=deprecated-declarations -Wa,--compress-debug-sections -fdiagnostics-color=always ";

if (os.environ.get("DEV_MACHINE") == "ts"):
  configs["CXX"] = "/usr/local/scaligent/toolchain/crosstool/v4/x86_64-unknown-linux-gnu/bin/x86_64-unknown-linux-gnu-g++";
  configs["LINKFLAGS"] = "-Wl,--compress-debug-sections=zlib -Wl,--dynamic-linker=/usr/local/scaligent/toolchain/crosstool/v4/x86_64-unknown-linux-gnu/x86_64-unknown-linux-gnu/sysroot/lib/ld-linux-x86-64.so.2 -B/usr/local/scaligent/toolchain/crosstool/v4/x86_64-unknown-linux-gnu/x86_64-unknown-linux-gnu/bin.gold -Wl,-rpath=/usr/local/scaligent/toolchain/crosstool/v4/x86_64-unknown-linux-gnu/x86_64-unknown-linux-gnu/sysroot/lib -Wl,--no-whole-archive ";