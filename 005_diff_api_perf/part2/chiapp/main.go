package main

import (
	"database/sql/driver"
	"encoding/json"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/go-chi/chi/v5"
)


type Parent struct {
	ID int64 `json:"-"`
	Title string `json:"title"`
	Description string `json:"description"`
	Created time.Time `json:"created"`
	Modified time.Time `json:"modified"`
}

type JsonField map[string]interface{}

func (m JsonField) Value() (driver.Value, error) {
    return json.Marshal(m)
}

func (m *JsonField) Scan(value interface{}) error {
    if value == nil {
        return nil
    }

    b, ok := value.([]byte)
    if !ok {
        log.Fatalf("Scan source was not []byte, got: %T", value)
    }

    return json.Unmarshal(b, &m)
}

type Child struct {
	ID int64 `json:"-"`
	ParentID int64 `json:"-"`
	Parent Parent `json:"parent"`
	Created time.Time `json:"created"`
	Modified time.Time `json:"modified"`
	Title string `json:"title"`
	JsonField JsonField `json:"json_field"`
	LongText string `json:"long_text"`
}

type Response struct {
	Count int64 `json:"count"`
	Results []Child `json:"results"`
	Next string `json:"next"`
	Previous string `json:"previous"`
}

var response Response

func GetChildren(w http.ResponseWriter, r *http.Request) {

	w.Header().Set("Content-Type", "application/json")
	
	
	json.NewEncoder(w).Encode(&response)
}



func main() {
	content, _ := os.ReadFile("./test_data.json")

	json.Unmarshal(content, &response);

    r := chi.NewRouter()
    r.Get("/children", GetChildren)
    http.ListenAndServe(":8003", r)
}
