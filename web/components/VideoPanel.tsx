import React, { useEffect, useRef, useCallback, useState } from 'react';
import { Camera, PhoneOff } from 'lucide-react';

interface VideoPanelProps {
  /** Called with SDP offer/answer/ICE payload to relay via WebSocket */
  onSignal: (signal: { signal_type: string; payload: Record<string, unknown> }) => void;
  /** Incoming signal from a remote peer (relayed from backend) */
  incomingSignal?: { signal_type: string; payload: Record<string, unknown> };
  peerId: string;
}

export const VideoPanel: React.FC<VideoPanelProps> = ({ onSignal, incomingSignal, peerId }) => {
  const localVideoRef = useRef<HTMLVideoElement>(null);
  const remoteVideoRef = useRef<HTMLVideoElement>(null);
  const pcRef = useRef<RTCPeerConnection | null>(null);
  const [camActive, setCamActive] = useState(false);
  const [status, setStatus] = useState<'idle' | 'calling' | 'connected'>('idle');

  const startCamera = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
      if (localVideoRef.current) localVideoRef.current.srcObject = stream;
      setCamActive(true);

      const pc = new RTCPeerConnection({
        iceServers: [{ urls: 'stun:stun.l.google.com:19302' }],
      });
      pcRef.current = pc;

      stream.getTracks().forEach((track) => pc.addTrack(track, stream));

      pc.onicecandidate = (event) => {
        if (event.candidate) {
          onSignal({
            signal_type: 'ice',
            payload: { candidate: event.candidate.toJSON(), peerId },
          });
        }
      };

      pc.ontrack = (event) => {
        if (remoteVideoRef.current) {
          remoteVideoRef.current.srcObject = event.streams[0];
          setStatus('connected');
        }
      };

      // Create and send offer
      const offer = await pc.createOffer();
      await pc.setLocalDescription(offer);
      onSignal({
        signal_type: 'offer',
        payload: { sdp: offer.sdp, type: offer.type, peerId },
      });
      setStatus('calling');
    } catch (err) {
      console.error('Camera error:', err);
    }
  }, [onSignal, peerId]);

  // Handle incoming signals
  useEffect(() => {
    if (!incomingSignal) return;

    (async () => {
      let pc = pcRef.current;
      const { signal_type, payload } = incomingSignal;

      if (signal_type === 'offer') {
        // Create peer connection if we don't have one yet (callee path)
        if (!pc) {
          pc = new RTCPeerConnection({
            iceServers: [{ urls: 'stun:stun.l.google.com:19302' }],
          });
          pcRef.current = pc;

          const localStream = localVideoRef.current?.srcObject as MediaStream | null;
          if (localStream) {
            localStream.getTracks().forEach((track) => pc!.addTrack(track, localStream));
          }

          pc.onicecandidate = (event) => {
            if (event.candidate) {
              onSignal({
                signal_type: 'ice',
                payload: { candidate: event.candidate.toJSON(), peerId },
              });
            }
          };

          pc.ontrack = (event) => {
            if (remoteVideoRef.current) {
              remoteVideoRef.current.srcObject = event.streams[0];
              setStatus('connected');
            }
          };
        }

        await pc.setRemoteDescription(
          new RTCSessionDescription(payload as unknown as RTCSessionDescriptionInit),
        );
        const answer = await pc.createAnswer();
        await pc.setLocalDescription(answer);
        onSignal({
          signal_type: 'answer',
          payload: { sdp: answer.sdp, type: answer.type, peerId },
        });
      } else if (signal_type === 'answer') {
        pc = pcRef.current;
        if (!pc) return;
        await pc.setRemoteDescription(
          new RTCSessionDescription(payload as unknown as RTCSessionDescriptionInit),
        );
      } else if (signal_type === 'ice') {
        pc = pcRef.current;
        if (!pc) return;
        await pc.addIceCandidate(new RTCIceCandidate(payload['candidate'] as RTCIceCandidateInit));
      }
    })();
  }, [incomingSignal, onSignal, peerId]);

  const hangUp = useCallback(() => {
    pcRef.current?.close();
    pcRef.current = null;
    if (localVideoRef.current?.srcObject) {
      (localVideoRef.current.srcObject as MediaStream).getTracks().forEach((t) => t.stop());
      localVideoRef.current.srcObject = null;
    }
    setCamActive(false);
    setStatus('idle');
  }, []);

  return (
    <div className="flex flex-col gap-2 bg-os-window border border-os-border rounded-xl p-3">
      <div className="flex gap-2">
        <video
          ref={localVideoRef} autoPlay muted playsInline
          className="w-1/2 rounded-lg bg-black aspect-video object-cover"
        />
        <video
          ref={remoteVideoRef} autoPlay playsInline
          className="w-1/2 rounded-lg bg-black aspect-video object-cover"
        />
      </div>
      <div className="flex items-center gap-2 justify-center">
        {!camActive ? (
          <button onClick={startCamera} className="flex items-center gap-2 px-3 py-1.5 bg-green-600 text-white rounded-lg text-sm hover:bg-green-700 transition-colors">
            <Camera size={16} /> Start Camera
          </button>
        ) : (
          <button onClick={hangUp} className="flex items-center gap-2 px-3 py-1.5 bg-red-600 text-white rounded-lg text-sm hover:bg-red-700 transition-colors">
            <PhoneOff size={16} /> Hang Up
          </button>
        )}
        <span className="text-xs text-os-text/60 capitalize">{status}</span>
      </div>
    </div>
  );
};
