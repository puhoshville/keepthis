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

Please ensure that you have memcached instance. 
I recommend you to use docker image for your first-time interactions with library:
```bash
docker run -d --rm -p 11211:11211 memcached
```
[More information about docker image](https://hub.docker.com/_/memcached)


### More examples

You can find out usages of KeepThis in `examples/` and `notebooks/`