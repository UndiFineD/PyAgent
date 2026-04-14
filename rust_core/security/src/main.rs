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

use aes_gcm::{aead::Aead, Aes256Gcm, KeyInit, Nonce};
use anyhow::{Context, Result};
use base64::{engine::general_purpose, Engine as _};
use clap::{Parser, Subcommand};
use rand_core::{OsRng, RngCore};
use std::{fs, path::PathBuf};

const KEY_LEN: usize = 32;
const NONCE_LEN: usize = 12;

#[derive(Parser)]
#[command(author, version, about, long_about = None)]
struct Args {
    #[command(subcommand)]
    cmd: Command,
}

#[derive(Subcommand)]
enum Command {
    /// Generate a new symmetric key and store it in the given file.
    Keygen { #[arg(long)] key_file: PathBuf },
    /// Encrypt a plaintext string and output Base64 ciphertext.
    Encrypt {
        #[arg(long)]
        key_file: PathBuf,
        #[arg(long)]
        plaintext: String,
    },
    /// Decrypt Base64 ciphertext.
    Decrypt {
        #[arg(long)]
        key_file: PathBuf,
        #[arg(long)]
        ciphertext: String,
    },
    /// Rotate the key stored in the given file.
    Rotate { #[arg(long)] key_file: PathBuf },
}

fn main() -> Result<()> {
    let args = Args::parse();

    match args.cmd {
        Command::Keygen { key_file } => generate_key(&key_file),
        Command::Encrypt { key_file, plaintext } => {
            let cipher = encrypt(&key_file, plaintext.as_bytes())?;
            println!("{}", cipher);
            Ok(())
        }
        Command::Decrypt { key_file, ciphertext } => {
            let plain = decrypt(&key_file, &ciphertext)?;
            println!("{}", String::from_utf8_lossy(&plain));
            Ok(())
        }
        Command::Rotate { key_file } => rotate_key(&key_file),
    }
}

fn load_key(path: &PathBuf) -> Result<[u8; KEY_LEN]> {
    let data = fs::read_to_string(path)
        .with_context(|| format!("failed to read key file {}", path.display()))?;
    let decoded = general_purpose::STANDARD
        .decode(data.trim())
        .context("failed to decode base64 key")?;
    let bytes: [u8; KEY_LEN] = decoded
        .as_slice()
        .try_into()
        .context("key file does not contain 32 bytes")?;
    Ok(bytes)
}

fn save_key(path: &PathBuf, key: &[u8; KEY_LEN]) -> Result<()> {
    let encoded = general_purpose::STANDARD.encode(key);
    fs::write(path, encoded).with_context(|| format!(
        "failed to write key file {}", path.display()))
}

fn generate_key(path: &PathBuf) -> Result<()> {
    let mut key = [0u8; KEY_LEN];
    OsRng.fill_bytes(&mut key);
    save_key(path, &key)
}

fn rotate_key(path: &PathBuf) -> Result<()> {
    generate_key(path)
}

fn encrypt(path: &PathBuf, plaintext: &[u8]) -> Result<String> {
    let key = load_key(path)?;
    let cipher = Aes256Gcm::new_from_slice(&key)
        .map_err(|e| anyhow::anyhow!("invalid key length: {e}"))?;
    let mut nonce = [0u8; NONCE_LEN];
    OsRng.fill_bytes(&mut nonce);
    let ciphertext = cipher
        .encrypt(Nonce::from_slice(&nonce), plaintext)
        .map_err(|e| anyhow::anyhow!("encryption failed: {e}"))?;
    let mut out = Vec::new();
    out.extend_from_slice(&nonce);
    out.extend_from_slice(&ciphertext);
    Ok(general_purpose::STANDARD.encode(out))
}

fn decrypt(path: &PathBuf, ciphertext: &str) -> Result<Vec<u8>> {
    let key = load_key(path)?;
    let bytes = general_purpose::STANDARD
        .decode(ciphertext)
        .context("failed to decode base64 ciphertext")?;
    if bytes.len() < NONCE_LEN {
        anyhow::bail!("ciphertext too short")
    }
    let (nonce, encrypted) = bytes.split_at(NONCE_LEN);
    let cipher = Aes256Gcm::new_from_slice(&key)
        .map_err(|e| anyhow::anyhow!("invalid key length: {e}"))?;
    let plaintext = cipher
        .decrypt(Nonce::from_slice(nonce), encrypted)
        .map_err(|e| anyhow::anyhow!("decryption failed: {e}"))?;
    Ok(plaintext)
}
