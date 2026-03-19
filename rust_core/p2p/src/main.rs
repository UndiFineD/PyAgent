use clap::Parser;
use libp2p::core::upgrade;
use libp2p::futures::StreamExt;
use libp2p::identity;
use libp2p::Transport;
use libp2p::noise;
use libp2p::ping::{Behaviour, Config, Event};
use libp2p::swarm::{Swarm, SwarmEvent};
use libp2p::tcp::{GenTcpConfig, TokioTcpTransport};
use libp2p::yamux;
use libp2p::Multiaddr;
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

    let key = identity::Keypair::generate_ed25519();
    let peer_id = key.public().to_peer_id();

    println!("Peer ID: {peer_id}");

    let transport = TokioTcpTransport::new(GenTcpConfig::new())
        .upgrade(upgrade::Version::V1)
        .authenticate(noise::NoiseAuthenticated::xx(&key).unwrap())
        .multiplex(yamux::YamuxConfig::default())
        .boxed();

    let behaviour = Behaviour::new(Config::new().with_interval(Duration::from_secs(5)));

    let mut swarm = Swarm::new(transport, behaviour, peer_id);

    let listen_addr = args.listen.parse()?;
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
            SwarmEvent::Behaviour(Event { peer, result }) => {
                println!("Ping event: {peer:?} -> {result:?}");
            }
            _ => {}
        }
    }

    Ok(())
}
