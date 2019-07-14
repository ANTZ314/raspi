

void outputBinary (int value)
{
	if ((value & 0x01) == 0) digitalWrite (17, 0) else digitalWrite (17, 1) ;	// 0000 0001
	if ((value & 0x02) == 0) digitalWrite (18, 0) else digitalWrite (18, 1) ;	// 0000 0010
	if ((value & 0x04) == 0) digitalWrite (21, 0) else digitalWrite (21, 1) ;	// 0000 0100
	if ((value & 0x08) == 0) digitalWrite (17, 0) else digitalWrite (17, 1) ;	// 0000 1000
	if ((value & 0x10) == 0) digitalWrite (17, 0) else digitalWrite (17, 1) ;	// 0001 0000
	if ((value & 0x20) == 0) digitalWrite (18, 0) else digitalWrite (18, 1) ;	// 0010 0000
	if ((value & 0x40) == 0) digitalWrite (21, 0) else digitalWrite (21, 1) ;	// 0100 0000
	if ((value & 0x80) == 0) digitalWrite (17, 0) else digitalWrite (17, 1) ;	// 1000 0000
}
