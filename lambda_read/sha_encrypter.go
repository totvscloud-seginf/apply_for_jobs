package main

import (
	"crypto/rand"
	"crypto/rsa"
	"crypto/tls"
	"crypto/x509"
	"os"
)

func NewShaEncrypter() (Encrypter, error) {

	keyPair, err := tls.LoadX509KeyPair(os.Getenv("CERT_PATH"), os.Getenv("PRIVATE_KEY_PATH"))
	if err != nil {
		return nil, err
	}

	keyPair.Leaf, err = x509.ParseCertificate(keyPair.Certificate[0])
	if err != nil {
		return nil, err
	}

	return ShaEncrypter{
		KeyPair: keyPair,
	}, nil

}

type ShaEncrypter struct {
	KeyPair tls.Certificate
}

func (e ShaEncrypter) Encrypt(plainText string) (string, error) {

	cipherTextBytes, err := rsa.EncryptPKCS1v15(rand.Reader, e.KeyPair.Leaf.PublicKey.(*rsa.PublicKey), []byte(plainText))

	return string(cipherTextBytes), err

}

func (s ShaEncrypter) Decrypt(cipherText string) (string, error) {

	plainTextBytes, err := rsa.DecryptPKCS1v15(rand.Reader, s.KeyPair.PrivateKey.(*rsa.PrivateKey), []byte(cipherText))

	return string(plainTextBytes), err

}
