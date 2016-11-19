#include <stdlib.h>
#include "context.h"

struct mem_alloc_node * create_mem_alloc_node(size_t mem_size) {
    struct mem_alloc_node *new_node = malloc(sizeof(struct mem_alloc_node));

    if(mem_size == 0) new_node -> mem = NULL;
    else new_node -> mem = malloc(mem_size);

    new_node -> mem_size = mem_size;
    new_node -> next = NULL;

    return new_node;
}

struct context * create_context() {
    struct context *new_context = malloc(sizeof(struct context));

    new_context -> mem_alloc_list_head = NULL;

    return new_context;
}

void destroy_context(struct context *cxt) {
    struct mem_alloc_node *current_node, *next_node;

    current_node = cxt -> mem_alloc_list_head;

    while(current_node != NULL) {
        next_node = current_node -> next;
        if(current_node -> mem) free(current_node -> mem);
        free(current_node);
        current_node = next_node;
    }

    free(cxt);
}

char * allocate_mem(struct context *cxt, size_t size) {
    struct mem_alloc_node *prev_head;

    if(cxt == NULL || size == 0) return NULL;

    prev_head = cxt -> mem_alloc_list_head;
    cxt -> mem_alloc_list_head = create_mem_alloc_node(size);
    cxt -> mem_alloc_list_head -> next = prev_head;

    return cxt -> mem_alloc_list_head -> mem;
}