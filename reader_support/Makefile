CFLAGS := -O2 -fPIC

read_card_uid: read_uid.o context.o
	$(CC) -shared -o read_uid.so read_uid.o context.o -lnfc

clean:
	rm *.o *.so
