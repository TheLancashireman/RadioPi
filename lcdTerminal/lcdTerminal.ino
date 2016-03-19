#include <LiquidCrystal.h>

#define led1		13		// On-board LED connected to digital pin 13

#define lcd_d0		5		// Pins for LCD display
#define lcd_d1		6
#define lcd_d2		7
#define lcd_d3		8
#define lcd_d4		9
#define lcd_d5		10
#define lcd_d6		11
#define lcd_d7		12
#define lcd_e		4
#define lcd_rw		3
#define lcd_rs		2

#define lcd_nrows	4
#define lcd_ncols	20

LiquidCrystal lcd(lcd_rs, lcd_rw, lcd_e,
				  lcd_d0, lcd_d1, lcd_d2, lcd_d3,
				  lcd_d4, lcd_d5, lcd_d6, lcd_d7);

unsigned long then;
char ledState;

char *lcdRows[lcd_nrows];
char lcdBuf[lcd_nrows*lcd_ncols];

int row, col;

void LcdPutc(int ch);
void LcdScrollUp(void);

void setup(void)
{
	int i;

	pinMode(led1, OUTPUT);			// Sets the digital pin as output
	digitalWrite(led1, LOW);		// Drive the pin low (LED off)
	ledState = 0;

	Serial.begin(9600);				// Start the serial port.
	Serial.println("Hello world!");	// ToDo : it'll need a "who are you?" response

	lcd.begin(lcd_ncols, lcd_nrows);	// Start the lcd driver
	lcd.setCursor(0, 0);				// Cursor to top left.
	lcd.print("Hello world!");

	Serial.println("DBG!");
	
	row = 3;						// Cursor to bottom left.
	col = 0;
	lcd.setCursor(col, row);
	for ( i=0; i<lcd_nrows; i++ )	// Initialise LCD buffers
	{
		lcdRows[i] = &lcdBuf[i*lcd_ncols];
	}

	Serial.println("DBG!");

	then = millis();				// Initialise the time reference.
}

void loop(void)
{
	unsigned long now = millis();
	unsigned long elapsed = now - then;
	int ch;

	if ( ledState )
	{
		// LED stays on for 20 ms
		if ( elapsed > 20 )
		{
			then += 20;
			ledState = 0;
			digitalWrite(led1, LOW);
		}
	}
	else
	{
		// LED stays off for 2 secs minus 20 ms
		if ( elapsed >= 1980 )
		{
			then += 1980;
			ledState = 1;
			digitalWrite(led1, HIGH);
		}
	}

	ch = Serial.read();
	if ( ch >= 0 )
	{
		LcdPutc(ch);
	}
}

void LcdPutc(int ch)
{
	if ( ch == '\r' )
	{
		col = 0;
		lcd.setCursor(col, row);
	}
	else
	if ( ch == '\n' )
	{
		if ( row >= 3 )
		{
			row = 3;		// Defensive
			LcdScrollUp();
		}
		else
		{
			row++;
		}
		lcd.setCursor(col, row);
	}
	else
	if ( col < 20 )
	{
		lcdRows[row][col] = ch;
		lcd.write(ch);
		col++;
	}
	else
	{
		// Ignore everything to the right of column 19
	}
}

void LcdScrollUp(void)
{
	lcd.clear();				// I hate this!
	char *tmp = lcdRows[0];
	int i, j;

	for ( i = 0; i < (lcd_nrows-1); i++ )
	{
		lcdRows[i] = lcdRows[i+1];
		lcd.setCursor(0, i);
		for ( j=0; j<lcd_ncols && lcdRows[i][j] != '\0'; j++ )
		{
			lcd.write(lcdRows[i][j]);
		}
	}

	for ( j=0; j<lcd_ncols; j++ )
	{
		tmp[j] = '\0';
	}

	lcdRows[lcd_nrows-1] = tmp;
}
