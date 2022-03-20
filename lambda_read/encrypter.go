package main

type Encrypter interface {
	Encrypt(plainText string) (string, error)
	Decrypt(cipherText string) (string, error)
}
