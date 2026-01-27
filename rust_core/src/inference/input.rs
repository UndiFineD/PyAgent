use pyo3::prelude::*;
use pyo3::types::{PyDict, PyList, PyTuple};
use std::collections::HashMap;

// =============================================================================
// Input Preprocessing & Chat Formatting
// =============================================================================

struct ChatMessage {
    role: String,
    content: String,
}

fn extract_messages(messages: &Bound<'_, PyList>) -> PyResult<Vec<ChatMessage>> {
    let mut result = Vec::with_capacity(messages.len());
    for item in messages.iter() {
        if let Ok(dict) = item.downcast::<PyDict>() {
            let role = dict.get_item("role")?.map(|s| s.extract::<String>()).transpose()?.unwrap_or_else(|| "user".to_string());
            let content = dict.get_item("content")?.map(|s| s.extract::<String>()).transpose()?.unwrap_or_default();
            result.push(ChatMessage { role, content });
        } else if let Ok(tuple) = item.downcast::<PyTuple>() {
            if tuple.len() >= 2 {
                let role = tuple.get_item(0)?.extract::<String>().unwrap_or_else(|_| "user".to_string());
                let content = tuple.get_item(1)?.extract::<String>().unwrap_or_default();
                result.push(ChatMessage { role, content });
            }
        }
    }
    Ok(result)
}

/// Linearize chat messages into a single string with chat template
#[pyfunction]
#[pyo3(signature = (messages, template_format, add_generation_prompt=None))]
pub fn linearize_chat_rust(
    messages: &Bound<'_, PyList>,
    template_format: &str, // "chatml", "alpaca", "llama2", "vicuna"
    add_generation_prompt: Option<bool>,
) -> PyResult<String> {
    let msg_list = extract_messages(messages)?;
    let add_gen_prompt = add_generation_prompt.unwrap_or(false);
    
    let mut buffer = String::with_capacity(msg_list.len() * 100);
    
    match template_format {
        "chatml" => {
            // <|im_start|>role\ncontent<|im_end|>\n
            for msg in &msg_list {
                buffer.push_str("<|im_start|>");
                buffer.push_str(&msg.role);
                buffer.push('\n');
                buffer.push_str(&msg.content);
                buffer.push_str("<|im_end|>\n");
            }
            if add_gen_prompt {
                buffer.push_str("<|im_start|>assistant\n");
            }
        }
        "llama2" | "mistral" => {
            // [INST] <<SYS>>\n{sys}\n<</SYS>>\n\n{usr} [/INST] {asst} </s><s>[INST] {usr} [/INST]
            let mut sys_msg = String::new();
            let mut first_user = true;
            
            for msg in &msg_list {
                match msg.role.as_str() {
                    "system" => {
                        sys_msg = msg.content.clone();
                    }
                    "user" => {
                        if first_user {
                            buffer.push_str("[INST] ");
                            if !sys_msg.is_empty() {
                                buffer.push_str("<<SYS>>\n");
                                buffer.push_str(&sys_msg);
                                buffer.push_str("\n<</SYS>>\n\n");
                            }
                            buffer.push_str(&msg.content);
                            buffer.push_str(" [/INST] ");
                            first_user = false;
                        } else {
                            buffer.push_str("<s>[INST] ");
                            buffer.push_str(&msg.content);
                            buffer.push_str(" [/INST] ");
                        }
                    }
                    "assistant" => {
                        buffer.push_str(&msg.content);
                        buffer.push_str(" </s>");
                    }
                    _ => {}
                }
            }
        }
        "llama" => {
            // Simple role: content format as expected by test
            for msg in &msg_list {
                buffer.push_str(&msg.role);
                buffer.push_str(": ");
                buffer.push_str(&msg.content);
                buffer.push('\n');
            }
        }
        "vicuna" => {
            // USER: {content} ASSISTANT: {content}</s>
            if !msg_list.is_empty() && msg_list[0].role == "system" {
                buffer.push_str(&msg_list[0].content);
                buffer.push('\n');
            }
            
            for msg in &msg_list {
                if msg.role == "system" { continue; }
                
                let prefix = if msg.role == "user" { "USER: " } else { "ASSISTANT: " };
                buffer.push_str(prefix);
                buffer.push_str(&msg.content);
                if msg.role == "assistant" {
                    buffer.push_str("</s>");
                }
                buffer.push('\n');
            }
            if add_gen_prompt {
                buffer.push_str("ASSISTANT: ");
            }
        }
        _ => { // alpaca logic as fallback for now
            // ### Instruction:\n{content}\n\n### Response:\n{content}
            for msg in &msg_list {
                match msg.role.as_str() {
                    "system" => {
                        buffer.push_str(&msg.content);
                        buffer.push_str("\n\n");
                    }
                    "user" => {
                        buffer.push_str("### Instruction:\n");
                        buffer.push_str(&msg.content);
                        buffer.push_str("\n\n");
                    }
                    "assistant" => {
                        buffer.push_str("### Response:\n");
                        buffer.push_str(&msg.content);
                        buffer.push_str("\n\n");
                    }
                    _ => {}
                }
            }
            if add_gen_prompt {
                buffer.push_str("### Response:\n");
            }
        }
    }
    
    Ok(buffer)
}

/// Validate chat message structure and roles
#[pyfunction]
#[pyo3(signature = (messages, allowed_roles=vec!["system".to_string(), "user".to_string(), "assistant".to_string()]))]
pub fn validate_chat_messages_rust(
    messages: &Bound<'_, PyList>,
    allowed_roles: Vec<String>,
) -> PyResult<(bool, String)> {
    if messages.is_empty() {
        return Ok((false, "Empty message list".to_string()));
    }

    for (i, item) in messages.iter().enumerate() {
        let (role, content) = if let Ok(dict) = item.downcast::<PyDict>() {
             if !dict.contains("role")? || !dict.contains("content")? {
                 return Ok((false, format!("Message {} missing role or content", i)));
             }
             let r = dict.get_item("role")?.map(|s| s.extract::<String>()).transpose()?.unwrap_or_default();
             let c = dict.get_item("content")?.map(|s| s.extract::<String>()).transpose()?.unwrap_or_default();
             (r, c)
        } else if let Ok(tuple) = item.downcast::<PyTuple>() {
             if tuple.len() != 2 {
                  continue; // Or error? Test says "invalid role" is caught.
             }
             let r = tuple.get_item(0)?.extract::<String>()?;
             let c = tuple.get_item(1)?.extract::<String>()?;
             (r, c)
        } else {
             return Ok((false, format!("Message {} invalid type", i)));
        };

        if !allowed_roles.contains(&role) {
            return Ok((false, format!("Message {} has invalid role '{}'", i, role)));
        }

        if content.trim().is_empty() {
            // warning
        }
        
        if role == "system" && i != 0 {
            // Warning
        }
    }

    Ok((true, String::new()))
}

/// Estimate token count for messages (heuristic without tokenizer)
#[pyfunction]
pub fn estimate_tokens_from_messages_rust(
    messages: &Bound<'_, PyList>,
    chars_per_token: f64,
) -> PyResult<usize> {
    let msg_list = extract_messages(messages)?;
    let mut total_chars = 0;
    for msg in msg_list {
        total_chars += msg.content.len();
        // Add overhead for wrappers
        total_chars += 10; 
    }
    
    Ok((total_chars as f64 / chars_per_token).ceil() as usize)
}

/// Truncate conversation history to fit context window
#[pyfunction]
pub fn truncate_chat_history_rust(
    messages: &Bound<'_, PyList>,
    max_tokens: usize,
    chars_per_token: f64,
    preserve_system: bool,
) -> PyResult<Vec<HashMap<String, String>>> {
    let mut msg_list = extract_messages(messages)?;
    // Estimate
    let mut total_chars = 0;
    for msg in &msg_list {
        total_chars += msg.content.len() + 10;
    }
    let estimated_total = (total_chars as f64 / chars_per_token).ceil() as usize;
    
    // We construct the output format (Dicts)
    let to_dict = |m: ChatMessage| {
        let mut map = HashMap::new();
        map.insert("role".to_string(), m.role);
        map.insert("content".to_string(), m.content);
        map
    };

    if estimated_total <= max_tokens {
         // Return as list of dicts
         return Ok(msg_list.into_iter().map(to_dict).collect());
    }
    
    let mut result_list = Vec::new();
    let mut current_tokens = 0;
    let mut system_msg = None;

    if preserve_system && !msg_list.is_empty() {
        if msg_list[0].role == "system" {
            let sys = msg_list.remove(0);
            let sys_tokens = (sys.content.len() + 10) as f64 / chars_per_token;
            current_tokens += sys_tokens.ceil() as usize;
            system_msg = Some(sys);
        }
    }

    // Add messages from end until full
    for msg in msg_list.into_iter().rev() {
        let msg_tokens = ((msg.content.len() + 10) as f64 / chars_per_token).ceil() as usize;
        if current_tokens + msg_tokens > max_tokens {
            break;
        }
        result_list.push(msg);
        current_tokens += msg_tokens;
    }

    result_list.reverse();

    if let Some(sys) = system_msg {
        result_list.insert(0, sys);
    }
    
    Ok(result_list.into_iter().map(to_dict).collect())
}

/// Mask padding tokens in input ids
#[pyfunction]
pub fn pad_input_ids_rust(
    input_ids: Vec<Vec<i64>>,
    pad_token_id: i64,
    padding_side: &str, // "left" or "right"
    max_len: Option<usize>,
) -> (Vec<Vec<i64>>, Vec<Vec<i64>>) { // (padded_ids, attention_mask)
    let batch_size = input_ids.len();
    let max_seq_len = max_len.unwrap_or_else(|| {
        input_ids.iter().map(|s| s.len()).max().unwrap_or(0)
    });

    let mut padded_ids = vec![vec![pad_token_id; max_seq_len]; batch_size];
    let mut attention_mask = vec![vec![0; max_seq_len]; batch_size];

    for (i, seq) in input_ids.iter().enumerate() {
        let seq_len = seq.len().min(max_seq_len);
        let start_idx = if padding_side == "left" {
            max_seq_len - seq_len
        } else {
            0
        };

        for (j, &token) in seq.iter().enumerate().take(seq_len) {
            padded_ids[i][start_idx + j] = token;
            attention_mask[i][start_idx + j] = 1;
        }
    }

    (padded_ids, attention_mask)
}

/// Extract thinking blocks from text using delimiters
/// Returns list of (start, end, content) tuples
#[pyfunction]
pub fn extract_thinking_blocks_rust(
    text: &str,
    open_tag: &str,
    close_tag: &str,
) -> Vec<(usize, usize, String)> {
    let mut blocks = Vec::new();
    let mut search_start = 0;

    while let Some(start) = text[search_start..].find(open_tag) {
        let abs_start = search_start + start;
        let content_start = abs_start + open_tag.len();

        if let Some(end) = text[content_start..].find(close_tag) {
            let abs_end = content_start + end;
            let content = text[content_start..abs_end].to_string();
            blocks.push((abs_start, abs_end + close_tag.len(), content));
            search_start = abs_end + close_tag.len();
        } else {
            break;
        }
    }

    blocks
}

/// Streaming-safe token classification for reasoning
/// Returns (is_thinking, is_tool_call, is_content)
#[pyfunction]
pub fn classify_token_context_rust(
    prefix: &str,
    token_text: &str,
    thinking_open: &str,
    thinking_close: &str,
) -> (bool, bool, bool) {
    let combined = format!("{}{}", prefix, token_text);

    // Check if we're inside thinking block
    let open_count = combined.matches(thinking_open).count();
    let close_count = combined.matches(thinking_close).count();
    let is_thinking = open_count > close_count;

    // Check if token is part of tool call
    let is_tool_call = combined.contains("\"name\"") &&
                       (combined.ends_with("\"arguments\"") ||
                        combined.contains("\"arguments\":"));

    // Content is default
    let is_content = !is_thinking && !is_tool_call;

    (is_thinking, is_tool_call, is_content)
}
