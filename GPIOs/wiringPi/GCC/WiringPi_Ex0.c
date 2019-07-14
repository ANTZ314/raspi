/* To Complile: 
 * gcc -o blinker blinker.c -l wiringPi
 * sudo ./blinker
 */

#include <stdio.h>    		// Used for printf() statements
#include <wiringPi.h> 		// Include WiringPi library!

// Pin number declarations. We're using the Broadcom chip pin numbers.
const int ledPin = 23; 		// Regular LED - Broadcom pin 23, P1 pin 16

int main(void)
{
    // Setup stuff:
    wiringPiSetupGpio(); 		// Initialize wiringPi -- using Broadcom pin numbers

    pinMode(ledPin, OUTPUT);     	// Set regular LED as output

    printf("Blinker is running! Press CTRL+C to quit.\n");

    // Loop (while(1)):
    while(1)
    {
            digitalWrite(ledPin, HIGH); // Turn LED ON
            delay(1000); // Wait 75ms
            digitalWrite(ledPin, LOW); // Turn LED OFF
            delay(1000); // Wait 75ms again
    }

    return 0;
}
