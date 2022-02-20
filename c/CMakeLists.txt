cmake_minimum_required(VERSION 3.13)

# initialize the SDK based on PICO_SDK_PATH
# note: this must happen before project()
include(pico_sdk_import.cmake)

project(main)

# initialize the Raspberry Pi Pico SDK
pico_sdk_init()

add_executable(main

pio_spi.c
pio_spi.h
main.c
)


# Compile PIO program
#pico_generate_pio_header(hello_world ${CMAKE_CURRENT_LIST_DIR}/hello.pio)
pico_generate_pio_header(main ${CMAKE_CURRENT_LIST_DIR}/spi.pio)

# Add pico_stdlib library which aggregates commonly used features
target_link_libraries(main pico_stdlib hardware_pio)

# enable usb output, disable uart output
pico_enable_stdio_usb(main 1)
pico_enable_stdio_uart(main 0)

# create map/bin/hex/uf2 file in addition to ELF.
pico_add_extra_outputs(main)


# add url via pico_set_program_url
# example_auto_set_url(hello_world)