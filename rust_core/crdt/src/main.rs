// Copyright 2026 PyAgent Authors
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

use anyhow::{Context, Result};
use automerge::{AutoCommit, ObjId, ObjType, ReadDoc, ScalarValue};
use automerge::hydrate::Value as HydrateValue;
use automerge::transaction::Transactable;
use base64::engine::general_purpose;
use base64::Engine as _;
use clap::{Parser, Subcommand};
use serde_json::Value;
use std::{fs, path::PathBuf};

/// A tiny CLI for CRDT merge experimentation.
#[derive(Parser)]
#[command(author, version, about, long_about = None)]
struct Args {
    #[command(subcommand)]
    cmd: Command,
}

#[derive(Subcommand)]
enum Command {
    /// Merge two JSON documents and print the merged JSON.
    Merge {
        #[arg(long)]
        left: PathBuf,
        #[arg(long)]
        right: PathBuf,
    },
}

fn main() -> Result<()> {
    let args = Args::parse();

    match args.cmd {
        Command::Merge { left, right } => {
            let left_json = read_json(&left)?;
            let right_json = read_json(&right)?;
            let merged = merge_crdt(&left_json, &right_json)?;
            println!("{}", serde_json::to_string(&merged)?)
        }
    }

    Ok(())
}

fn read_json(path: &PathBuf) -> Result<Value> {
    let data = fs::read_to_string(path)
        .with_context(|| format!("failed to read JSON file {}", path.display()))?;
    Ok(serde_json::from_str(&data)
        .with_context(|| format!("failed to parse JSON from {}", path.display()))?)
}

fn merge_crdt(left: &Value, right: &Value) -> Result<Value> {
    let mut doc_a = json_to_automerge(left)?;
    let mut doc_b = json_to_automerge(right)?;
    doc_a
        .merge(&mut doc_b)
        .context("failed to merge automerge documents")?;
    automerge_to_json(&doc_a)
}

fn automerge_to_json(doc: &AutoCommit) -> Result<Value> {
    let hydrated = doc.hydrate(ObjId::Root, None)?;
    hydrate_to_json(&hydrated)
}

fn json_to_automerge(json: &Value) -> Result<AutoCommit> {
    let mut doc = AutoCommit::new();
    apply_json_to_doc(&mut doc, &ObjId::Root, json)?;
    Ok(doc)
}

fn hydrate_to_json(value: &HydrateValue) -> Result<Value> {
    Ok(match value {
        HydrateValue::Scalar(s) => match s {
            ScalarValue::Null => Value::Null,
            ScalarValue::Boolean(b) => Value::Bool(*b),
            ScalarValue::Int(i) => Value::Number((*i).into()),
            ScalarValue::Uint(u) => Value::Number((*u).into()),
            ScalarValue::F64(f) => serde_json::Number::from_f64(*f)
                .map(Value::Number)
                .unwrap_or(Value::Null),
            ScalarValue::Str(s) => Value::String(s.to_string()),
            ScalarValue::Bytes(b) => Value::String(general_purpose::STANDARD.encode(b)),
            _ => Value::Null,
        },
        HydrateValue::Map(map) => {
            let mut out = serde_json::Map::new();
            for (k, v) in map.iter() {
                out.insert(k.clone(), hydrate_to_json(&v.value)?);
            }
            Value::Object(out)
        }
        HydrateValue::List(list) => {
            let mut out = Vec::new();
            for v in list.iter() {
                out.push(hydrate_to_json(&v.value)?);
            }
            Value::Array(out)
        }
        HydrateValue::Text(text) => Value::String(text.to_string()),
    })
}

fn apply_json_to_doc(doc: &mut AutoCommit, obj: &ObjId, json: &Value) -> Result<()> {
    match json {
        Value::Object(map) => {
            for (k, v) in map {
                match v {
                    Value::Object(_) => {
                        let new_obj = doc.put_object(obj, k, ObjType::Map)?;
                        apply_json_to_doc(doc, &new_obj, v)?;
                    }
                    Value::Array(_) => {
                        let new_obj = doc.put_object(obj, k, ObjType::List)?;
                        apply_json_to_doc(doc, &new_obj, v)?;
                    }
                    _ => {
                        if let Some(sv) = value_to_scalar(v)? {
                            doc.put(obj, k, sv)?;
                        }
                    }
                }
            }
        }
        Value::Array(arr) => {
            for v in arr {
                match v {
                    Value::Object(_) => {
                        let new_obj = doc.insert_object(obj, usize::MAX, ObjType::Map)?;
                        apply_json_to_doc(doc, &new_obj, v)?;
                    }
                    Value::Array(_) => {
                        let new_obj = doc.insert_object(obj, usize::MAX, ObjType::List)?;
                        apply_json_to_doc(doc, &new_obj, v)?;
                    }
                    _ => {
                        if let Some(sv) = value_to_scalar(v)? {
                            doc.insert(obj, usize::MAX, sv)?;
                        }
                    }
                }
            }
        }
        _ => {
            // top-level scalar, not expected.
        }
    }
    Ok(())
}

fn value_to_scalar(value: &Value) -> Result<Option<ScalarValue>> {
    Ok(match value {
        Value::Null => Some(ScalarValue::Null),
        Value::Bool(b) => Some(ScalarValue::Boolean(*b)),
        Value::Number(n) => {
            if let Some(i) = n.as_i64() {
                Some(ScalarValue::Int(i))
            } else if let Some(u) = n.as_u64() {
                Some(ScalarValue::Uint(u))
            } else if let Some(f) = n.as_f64() {
                Some(ScalarValue::F64(f))
            } else {
                None
            }
        }
        Value::String(s) => Some(ScalarValue::Str(s.clone().into())),
        _ => None,
    })
}
