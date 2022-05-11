import os
from rpython.rtyper.lltypesystem import rffi, lltype
from rpython.rlib import rdynload

path = './source/csource/hlib.so'
ll_libname = rffi.str2charp(path)
dll = rdynload.dlopen(ll_libname, rdynload._dlopen_default_mode())
lltype.free(ll_libname, flavor='raw')

initptr = rdynload.dlsym(dll, 'hello')
func_void_void = lltype.Ptr(lltype.FuncType([], lltype.Void))
helloFunc = rffi.cast(func_void_void, initptr)

helloFunc()

initptr = rdynload.dlsym(dll, 'printMyInt')
# https://rpython.readthedocs.io/en/latest/rtyper.html
IntStruct = lltype.GcStruct('MyInt', ('Int', lltype.Signed))
pIntStruct = lltype.malloc(IntStruct)
pIntStruct.Int = 23

func_void_MyInt = lltype.Ptr(lltype.FuncType([lltype.Ptr(IntStruct)], lltype.Void))
printMyInt = rffi.cast(func_void_MyInt, initptr)

printMyInt(pIntStruct)
