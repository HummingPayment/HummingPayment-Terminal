#include <stdlib.h>
#include <string.h>
#include <nfc/nfc.h>

#include "context.h"

static nfc_device *pnd = NULL;
static nfc_context *context = NULL;

static const char *hex_table = "0123456789abcdef";

static int convert_to_hex_string(unsigned char *data, size_t length, char *target) { // target.length should be at least data.length*2+1
  int i;
  int pos = 0;

  for(i = 0; i < length; i++) {
    target[pos] = hex_table[data[i] >> 4];
    target[pos + 1] = hex_table[data[i] & 15];
    pos += 2;
  }

  target[pos] = 0;
  return pos;
}

char * read_uid(struct context *cxt) {
  static const nfc_modulation nmMifare = {
    .nmt = NMT_ISO14443A,
    .nbr = NBR_106,
  };
  nfc_target nt;
  char *result;

  if(!pnd) return NULL;

  result = allocate_mem(cxt, 65);
  if(!result) return NULL;

  if (nfc_initiator_select_passive_target(pnd, nmMifare, NULL, 0, &nt) > 0) {
    if(nt.nti.nai.szUidLen > 32) return NULL;
    convert_to_hex_string(nt.nti.nai.abtUid, nt.nti.nai.szUidLen, result);
    return result;
  }

  return NULL;
}

void __attribute__((constructor)) module_init() {
  nfc_init(&context);
  if (context == NULL) {
    printf("Unable to init libnfc\n");
    exit(EXIT_FAILURE);
  }

  pnd = nfc_open(context, NULL);

  if (pnd == NULL) {
    printf("ERROR: %s\n", "Unable to open NFC device.");
    exit(EXIT_FAILURE);
  }
  if (nfc_initiator_init(pnd) < 0) {
    nfc_perror(pnd, "nfc_initiator_init");
    exit(EXIT_FAILURE);
  }

  printf("NFC reader: %s opened\n", nfc_device_get_name(pnd));
}

void __attribute__((destructor)) module_exit() {
  nfc_close(pnd);
  nfc_exit(context);
}
