import pyopencl as cl
import numpy as np

class CL :


    def __init__(self):
        self.ctx = cl.create_some_context()
        self.queue = cl.CommandQueue(self.ctx)

    def loadProgram(self, filename):
        # read in the OpenCL source file as a string
        f = open(filename, 'r')
        fstr = "".join(f.readlines())
        print fstr
        # create the program
        self.program = cl.Program(self.ctx, fstr).build()

    def envSetup(self, size):
        mf = cl.mem_flags

        # initialize client side (CPU) arrays



        self.a = np.array(range(size), dtype=np.float32)
        self.b = np.array(range(size), dtype=np.float32)

        # create OpenCL buffers
        self.a_buf = cl.Buffer(self.ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=self.a)
        self.b_buf = cl.Buffer(self.ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=self.b)
        self.dest_buf = cl.Buffer(self.ctx, mf.WRITE_ONLY, self.b.nbytes)

    def execute(self):
        self.program.vec_add(self.queue, self.a.shape, None, self.a_buf, self.b_buf, self.dest_buf)
        c = np.empty_like(self.a)
        cl.enqueue_read_buffer(self.queue, self.dest_buf, c).wait()
        print c



if __name__ == "__main__":
    example = CL()
    example.loadProgram("vec_add.cl")
    example.envSetup(np.power(2,20))
    example.execute()