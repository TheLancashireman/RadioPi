
mmc_spi.dtbo:	mmc_spi.dts
	dtc -@ -I dts -O dtb -o mmc_spi.dtbo mmc_spi.dts

install:	mmc_spi.dtbo
	cp mmc_spi.dtbo /boot/overlays/mmc_spi.dtbo
