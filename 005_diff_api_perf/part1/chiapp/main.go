package main

import (
	"database/sql"
	"database/sql/driver"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"strconv"
	"time"

	"github.com/go-chi/chi/v5"
	"github.com/joho/godotenv"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

type Parent struct {
	ID int64 `gorm:"primaryKey" json:"-"`
	Title string `gorm:"type:varchar(64);" json:"title"`
	Description string `json:"description"`
	Created time.Time `json:"created"`
	Modified time.Time `json:"modified"`
}

func (Parent) TableName() string {
    return "testapp_parent"
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
	ID int64 `gorm:"primaryKey" json:"-"`
	ParentID int64 `gorm:"column:parent_id" json:"-"`
	Parent Parent `gorm:"associationForeignKey:ParentID;foreignKey:ParentID" json:"parent"`
	Created time.Time `json:"created"`
	Modified time.Time `json:"modified"`
	Title string `gorm:"type:varchar(64);" json:"title"`
	JsonField JsonField `gorm:"column:json_field;type:jsonb" json:"json_field"`
	LongText string `json:"long_text"`
}

func (Child) TableName() string {
    return "testapp_child"
}

type NullableStr struct {
	Value  string
	IsNull bool
}

func (ns NullableStr) MarshalJSON() ([]byte, error) {
	if ns.IsNull {
		return []byte("null"), nil
	}
	return json.Marshal(ns.Value)
}

type Response struct {
	Count int64 `json:"count"`
	Results []Child `json:"results"`
	Next NullableStr `json:"next"`
	Previous NullableStr `json:"previous"`
}


var pool *sql.DB
var db *gorm.DB

func GetChildren(w http.ResponseWriter, r *http.Request) {
	page := 1
	perPage := 30
	receivedPage, ok := r.URL.Query()["page"]
	if ok {
		p, err := strconv.Atoi(receivedPage[0])
		if err != nil {
			log.Fatal("Invalid page")
		}
		if p != page {
			page = p
		}
	}
	offset :=(page - 1) * perPage

	var children []Child
	var count int64
	query := db.Joins(
		"Parent")
	query.Model(&Child{}).Count(&count)

	w.Header().Set("Content-Type", "application/json")
	
	pages := int(count) / perPage
	if int(count) % perPage != 0 {
        pages += 1
	}
	host := r.Host
	path := r.URL.Path
	scheme := "http" // yep, cheating here, lazy to do it bullet proof
	baseUrl := fmt.Sprintf("%s://%s%s", scheme, host, path)
	nextPage := NullableStr{Value: "", IsNull: true}
	previousPage := NullableStr{Value: "", IsNull: true}

	if page < pages {
		nextPage.Value = fmt.Sprintf("%s?page=%d", baseUrl, page + 1)
		nextPage.IsNull = false
	}
	if page > 1 {
		previousPage.Value = fmt.Sprintf("%s?page=%d", baseUrl, page - 1)
		previousPage.IsNull = false
	}

	result := db.Joins("Parent").Limit(
			perPage).Offset(offset).Order(
			"testapp_child.id, testapp_child.parent_id").Find(&children)
	if result.Error != nil {
		log.Fatal("SELECT failed")
	}
	
	json.NewEncoder(w).Encode(&Response{Count: count, Results: children, Previous: previousPage, Next: nextPage})
}



func main() {
	var err error
	err = godotenv.Load("../.env")
    if err != nil {
        log.Fatal("couldn't load .env")
    }
    dsn := os.Getenv("DATABASE_URL")
	
	db, err = gorm.Open(postgres.Open(dsn), &gorm.Config{})
	if err != nil {
		log.Fatal("Could not connect to the database")
	}

	pool, err = db.DB()
	if err != nil {
		log.Fatal("pool failure")
	}
	pool.SetMaxIdleConns(10)
	pool.SetMaxOpenConns(20)


    r := chi.NewRouter()
    // r.Use(middleware.Logger)
    r.Get("/children", GetChildren)
    http.ListenAndServe(":8003", r)
}
