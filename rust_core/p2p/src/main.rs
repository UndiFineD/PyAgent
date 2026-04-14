use clap::Parser;
use libp2p::futures::StreamExt;
use libp2p::swarm::SwarmEvent;
use libp2p::{noise, ping, tcp, yamux, Multiaddr, SwarmBuilder};
use std::error::Error;
use std::time::Duration;

#[derive(Parser)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Multiaddr to listen on (default: /ip4/0.0.0.0/tcp/0)
    #[arg(long, default_value = "/ip4/0.0.0.0/tcp/0")]
    listen: String,

    /// Optional peer address to dial on startup.
    #[arg(long)]
    dial: Option<String>,
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let args = Args::parse();

    let mut swarm = SwarmBuilder::with_new_identity()
        .with_tokio()
        .with_tcp(
            tcp::Config::default(),
            noise::Config::new,
            yamux::Config::default,
        )?
        .with_behaviour(|_key| {
            Ok(ping::Behaviour::new(
                ping::Config::new().with_interval(Duration::from_secs(5)),
            ))
        })?
        .build();

    println!("Peer ID: {}", swarm.local_peer_id());

    let listen_addr: Multiaddr = args.listen.parse()?;
    swarm.listen_on(listen_addr)?;

    if let Some(dial_addr) = args.dial {
        let addr: Multiaddr = dial_addr.parse()?;
        swarm.dial(addr)?;
    }

    while let Some(event) = swarm.next().await {
        match event {
            SwarmEvent::NewListenAddr { address, .. } => {
                println!("Listening on {address}");
            }
            SwarmEvent::Behaviour(event) => {
                println!("Ping event: {event:?}");
            }
            _ => {}
        }
    }

    Ok(())
}
