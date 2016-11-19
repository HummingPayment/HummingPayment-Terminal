struct mem_alloc_node {
    char *mem;
    size_t mem_size;
    struct mem_alloc_node *next;
};

struct context {
    struct mem_alloc_node *mem_alloc_list_head;
};

struct mem_alloc_node * create_mem_alloc_node(size_t mem_size);
struct context * create_context();
void destroy_context(struct context *cxt);
char * allocate_mem(struct context *cxt, size_t size);