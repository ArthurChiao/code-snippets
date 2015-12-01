/**
 * properties of Sinleton:
 *
 * 1. 有一个指唯一实例的静态指针m_instance，并且是private
 * 2. 有一个public的函数，可以获取这个唯一的实例，并在需要的时候创建该实例
 * 3. 构造函数是private，这样就不能从别处创建该类的实例
 */
class Singleton {
    public:
        static Singleton* get_instance() {
            if (!m_instance) {
                m_instance = new Singleton();
            }
            return m_instance;
        }
        static void destroy() {
            delete m_instance;
            m_instance = NULL;
        }

    private:
        Singleton(){};
        static Singleton *m_instance;
}
