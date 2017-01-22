

__kernel void vec_add(global float* a, global float* b, global float* c)
{
    unsigned int i = get_global_id(0);

    c[i] = a[i] + b[i];
}