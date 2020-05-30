# KeepThis

![keepthis_header_gif](imgs/keepthis_header.gif)

## About project

Scientific toolkit which will inspire you and your team to work with more collaboration than ever before.

It works almost like LRU Cache but allows you:
1. Use same cache in different processes;
2. Use same cache at the different moments of time;
3. Easily share your local runtime's results with your teammates!  

Using [memcached](https://memcached.org) as a backend allows you to cache really large things.

## Try it!

### How to install

Using pip:

```bash
pip install keepthis
```

From source:
```bash
# 1. clone this repo
git clone https://github.com/puhoshville/keepthis.git

# 2. cd to repository's root directory
cd keepthis

# 3. install
pip install -e .
```

### How to setup local memcached server
 
I recommend you to use docker image for your first-time interactions with library:
```bash
docker run -d --rm -p 11211:11211 memcached
```
[More information about docker image](https://hub.docker.com/_/memcached)


### How to use KeepThis

! Before using KeepThis please make sure that you have memcached instance to store cache.

1. Import and initialize instance 
    ```python
    from keepthis import KeepThis

    
    keep = KeepThis('localhost', 11211)  # connect to local memcached instance
    ```
    
2. Define function with keepthis decorator
    ```python
    @keep.this
    def get_fibonacci(num):
        if num == 0:
            return 1
        if num == 1:
            return 1    
        return get_fibonacci(num-1) + get_fibonacci(num-2)

    ```
3. Done! All function execution's results will be stored in memcached and will be reused if nessecary. 

### More examples

You can find out usages of KeepThis in `examples/` and `notebooks/`