#include <stdio.h>
#include "pico/stdlib.h"
#include <string.h>
#include "hardware/adc.h"

void flash(uint8_t times) {
    for (uint8_t c = 0; c < times; c++) {
        gpio_put(PICO_DEFAULT_LED_PIN, 1);
        sleep_ms(25);
        gpio_put(PICO_DEFAULT_LED_PIN, 0);
        sleep_ms(100);
    }
}

int main() {
    char buffer[30];

    //Init
    stdio_init_all();

    //Set up LED pins
    gpio_init(PICO_DEFAULT_LED_PIN);
    gpio_set_dir(PICO_DEFAULT_LED_PIN, GPIO_OUT);

    //Set up temp sensor
    adc_init();
    adc_select_input(4);

    //We are alive
    flash(1);

    while (true) {
        const float conversion_factor = 3.3f / (1 << 12);
        float result = adc_read() * conversion_factor;
        result = 27 - (result - 0.706f)/0.001721f;
        //flash(1);
        //sleep_ms(200);



        memset(buffer, 0, sizeof(buffer));
        int16_t ch = getchar_timeout_us(0);
        if(ch != PICO_ERROR_TIMEOUT)
        {
            int i = 0;
            while(ch != PICO_ERROR_TIMEOUT)
            {
                buffer[i] = ch;
                ch = getchar_timeout_us(0);
                i++;
            }
            flash(1);
            printf("%s", buffer);
        }
        sleep_ms(100);
    }
    return 0;
}