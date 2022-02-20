/**
 * Copyright (c) 2020 Raspberry Pi (Trading) Ltd.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 */

#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/pio.h"
#include "pio_spi.h"
const uint OE_PIN = 1;
const uint SI_PIN = 3;
const uint SO_PIN = 4;
const uint CLK_PIN = 2;

int main() {
    stdio_init_all();
    
    stdio_set_translate_crlf(&stdio_usb, false);

    pio_spi_inst_t spi = {
            .pio = pio0,
            .sm = 0
    };
    uint cpha1_prog_offs = pio_add_program(spi.pio, &spi_cpha1_program);
    pio_spi_init(spi.pio, spi.sm, cpha1_prog_offs, 8, 4058.838, 1, 1, CLK_PIN, SO_PIN, SI_PIN);

    gpio_init(OE_PIN);

    gpio_set_dir(OE_PIN, GPIO_OUT);
    gpio_put(OE_PIN, 1);

    while(1) {
        //unsigned char tx = getchar();
        unsigned char tx = 'e';
        unsigned char rx;
        pio_spi_write8_read8_blocking(&spi, &tx, &rx, 1);
        putchar(rx);
    }

    return 0;
}
