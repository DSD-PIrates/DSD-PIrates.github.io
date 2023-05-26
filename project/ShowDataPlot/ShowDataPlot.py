import matplotlib.pyplot as plt

Y=[20,33,51,79,101,121,132,145,162,182,203,219,232,243,256,270,287,310,325, 237, 368]
def scatter_plot():
    # 打开交互模式
    plt.ion()
    for index in range(10):
        plt.cla()

        plt.title("Dynamic Diagram")
        plt.grid(True)

        plt.ylim(0, 500)
        plt.plot(list(range(index, index + 10)),Y[index: index + 10],'r--')

        plt.pause(1)

    plt.ioff()

    plt.show()

scatter_plot()