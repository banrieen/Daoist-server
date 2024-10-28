#[derive(Serialize, Deserialize)]
struct Movie {
  id: i64,
  title: String,
  poster: String,
  overview: String,
  release_date: i64,
  genres: Vec<String>
}
#[derive(Serialize, Deserialize)]
struct Movie {
  id: i64,
  #[serde(flatten)]
  value: serde_json::Value,
}
use meilisearch_sdk::{
    indexes::*,
    client::*,
    search::*,
    settings::*
  };
use serde::{Serialize, Deserialize};
use std::{io::prelude::*, fs::File};
use futures::executor::block_on;

fn info() { block_on(async move {
  let client = Client::new("http://localhost:7700", Some("aSampleMasterKey"));

  // reading and parsing the file
  let mut file = File::open("movies.json")
    .unwrap();
  let mut content = String::new();
  file
    .read_to_string(&mut content)
    .unwrap();
  let movies_docs: Vec<Movie> = serde_json::from_str(&content)
    .unwrap();

  // adding documents
  client
    .index("movies")
    .add_documents(&movies_docs, None)
    .await
    .unwrap();
})}
