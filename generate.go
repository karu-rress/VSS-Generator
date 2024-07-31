package main

import (
	"encoding/json"
	"fmt"
	"math/rand"
	"time"
)

type Vehicle struct {
	CarID     string `json:"car_id"`
	Speed     Speed  `json:"Speed"`
	Location  Location `json:"Location"`
	FuelLevel FuelLevel `json:"FuelLevel"`
	Engine    Engine  `json:"Engine"`
}

type Speed struct {
	Value int    `json:"value"`
	Unit  string `json:"unit"`
}

type Location struct {
	Latitude  float64 `json:"Latitude"`
	Longitude float64 `json:"Longitude"`
}

type FuelLevel struct {
	Value float64 `json:"value"`
	Unit  string  `json:"unit"`
}

type Engine struct {
	Temperature Temperature `json:"Temperature"`
}

type Temperature struct {
	Value float64 `json:"value"`
	Unit  string  `json:"unit"`
}

func randomVehicle() Vehicle {
	rand.Seed(time.Now().UnixNano())

	carID := "car_" + fmt.Sprintf("%d", rand.Intn(1000))
	speed := Speed{
		Value: rand.Intn(121), // 0 to 120 km/h
		Unit:  "km/h",
	}
	location := Location{
		Latitude:  rand.Float64()*180 - 90,  // -90 to 90
		Longitude: rand.Float64()*360 - 180, // -180 to 180
	}
	fuelLevel := FuelLevel{
		Value: rand.Float64() * 100, // 0 to 100%
		Unit:  "%",
	}
	engineTemperature := Engine{
		Temperature: Temperature{
			Value: float64(rand.Intn(121)), // 0 to 120 °C
			Unit:  "°C",
		},
	}

	return Vehicle{
		CarID:     carID,
		Speed:     speed,
		Location:  location,
		FuelLevel: fuelLevel,
		Engine:    engineTemperature,
	}
}

func main() {
	vehicle := randomVehicle()
	vehicleJSON, err := json.MarshalIndent(vehicle, "", "  ")
	if err != nil {
		fmt.Println("Error marshalling to JSON:", err)
		return
	}
	fmt.Println(string(vehicleJSON))
}
