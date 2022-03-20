package main

type Repository interface {
	Get(id string) (string, int, error)
	Remove(id string) error
	UpdateView(id string, views int) error
}
