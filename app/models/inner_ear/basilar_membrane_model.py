"""
Modelo de Vibração da Membrana Basilar
Baseado no modelo de osciladores massa-mola-amortecedor
Inspirado em von Békésy e Lesser-Berkeley
"""

import numpy as np
from scipy.signal import hilbert


class BasilarMembraneModel:
    """
    Modelo simplificado da membrana basilar usando osciladores acoplados
    """
    
    def __init__(self, n_sections=100, length=35e-3):
        """
        Inicializa o modelo da membrana basilar
        
        Parâmetros:
        -----------
        n_sections : int
            Número de seções ao longo da membrana basilar
        length : float
            Comprimento total da membrana basilar em metros (padrão: 35mm)
        """
        self.n_sections = n_sections
        self.length = length
        self.x = np.linspace(0, length, n_sections)  # Posições ao longo da MB
        
        # Parâmetros físicos que variam ao longo da membrana
        self._setup_physical_parameters()
        
    def _setup_physical_parameters(self):
        """
        Define os parâmetros físicos que variam ao longo da membrana basilar
        Baseado no mapa de Greenwood e propriedades mecânicas
        """
        # Mapa de frequências características (Greenwood, 1990)
        # CF(x) = A * (10^(ax) - k) onde x é normalizado
        A = 165.4  # Hz para humanos
        a = 2.1    # constante
        k = 0.88   # offset
        
        x_norm = self.x / self.length  # Normaliza posição (0 a 1)
        
        # Frequências características (Hz) - varia de ~20kHz (base) a ~20Hz (ápice)
        self.cf = A * (10**(a * (1 - x_norm)) - k)
        
        # Frequência angular característica
        self.omega_0 = 2 * np.pi * self.cf
        
        # Massa por unidade de área (kg/m²) - relativamente constante
        self.mass = 0.5e-3 * np.ones(self.n_sections)
        
        # Rigidez (N/m) - decresce exponencialmente da base ao ápice
        # k = m * omega_0^2
        self.stiffness = self.mass * self.omega_0**2
        
        # Amortecimento crítico para Q ≈ 3-10
        Q_factor = 5.0  # Fator de qualidade
        self.damping = self.omega_0 * self.mass / Q_factor
        
        # Acoplamento entre seções adjacentes (simplificado)
        self.coupling = 0.1 * self.stiffness[:-1]
        
    def greenwood_map(self, frequency):
        """
        Retorna a posição ao longo da MB para uma dada frequência
        usando o mapa de Greenwood invertido
        
        Parâmetros:
        -----------
        frequency : float
            Frequência em Hz
            
        Retorna:
        --------
        position : float
            Posição em metros
        """
        A = 165.4
        a = 2.1
        k = 0.88
        
        x_norm = (1.0 / a) * np.log10((frequency / A) + k)
        position = (1 - x_norm) * self.length
        
        return position
        
    def simulate_response(self, sound_signal, fs, duration=None):
        """
        Simula a resposta da membrana basilar a um sinal sonoro
        Usa filtros passa-banda de segunda ordem para cada seção
        
        Parâmetros:
        -----------
        sound_signal : array
            Sinal de entrada em Pascals
        fs : float
            Taxa de amostragem em Hz
        duration : float
            Duração da simulação (se None, usa todo o sinal)
            
        Retorna:
        --------
        t : array
            Vetor de tempo
        displacement : array (n_time x n_sections)
            Deslocamento da membrana em cada seção ao longo do tempo
        """
        from scipy.signal import butter, lfilter, sosfilt
        
        if duration is None:
            n_samples = len(sound_signal)
        else:
            n_samples = int(duration * fs)
            
        sound_signal = sound_signal[:n_samples]
        t = np.arange(n_samples) / fs
        
        # Inicializa array de deslocamento
        displacement = np.zeros((n_samples, self.n_sections))
        
        # Cada seção da membrana basilar age como um filtro passa-banda
        # centrado em sua frequência característica
        for j in range(self.n_sections):
            # Parâmetros do filtro para esta seção
            center_freq = self.cf[j]
            Q = 5.0  # Fator de qualidade
            
            # Largura de banda
            bw = center_freq / Q
            
            # Frequências de corte (evita problemas com freq muito baixas/altas)
            low_freq = max(center_freq - bw/2, 20)
            high_freq = min(center_freq + bw/2, fs/2 - 100)
            
            if low_freq >= high_freq or high_freq >= fs/2:
                # Pula seções problemáticas
                continue
            
            try:
                # Cria filtro passa-banda usando Butterworth de ordem 2
                sos = butter(2, [low_freq, high_freq], btype='band', 
                           fs=fs, output='sos')
                
                # Aplica filtro ao sinal
                filtered = sosfilt(sos, sound_signal)
                
                # Ganho baseado na resposta fisiológica típica
                # Deslocamentos típicos: 0.1-10 nm para 60 dB SPL
                gain = 1e-3 / (self.mass[j] * self.omega_0[j]**2)
                
                displacement[:, j] = filtered * gain
                
            except Exception as e:
                # Se houver erro, mantém zeros
                continue
        
        return t, displacement
    
    def analyze_frequency_response(self, frequencies, level_db=60):
        """
        Analisa a resposta em frequência da membrana basilar
        
        Parâmetros:
        -----------
        frequencies : array
            Array de frequências para testar (Hz)
        level_db : float
            Nível de pressão sonora em dB SPL
            
        Retorna:
        --------
        response_map : array (n_freq x n_sections)
            Amplitude de resposta para cada frequência em cada seção
        """
        # Converte dB SPL para Pascal
        p_ref = 20e-6  # Pressão de referência (20 μPa)
        pressure = p_ref * 10**(level_db / 20)
        
        response_map = np.zeros((len(frequencies), self.n_sections))
        
        for i, freq in enumerate(frequencies):
            omega = 2 * np.pi * freq
            
            # Resposta de cada oscilador a esta frequência
            # H(omega) = 1 / sqrt((k - m*omega^2)^2 + (c*omega)^2)
            for j in range(self.n_sections):
                numerator = pressure
                denominator = np.sqrt(
                    (self.stiffness[j] - self.mass[j] * omega**2)**2 + 
                    (self.damping[j] * omega)**2
                )
                response_map[i, j] = numerator / denominator
                
        return response_map


def create_pure_tone(frequency, duration, fs, amplitude_db=60):
    """
    Cria um tom puro
    
    Parâmetros:
    -----------
    frequency : float
        Frequência em Hz
    duration : float
        Duração em segundos
    fs : float
        Taxa de amostragem em Hz
    amplitude_db : float
        Amplitude em dB SPL
        
    Retorna:
    --------
    signal : array
        Sinal em Pascals
    """
    t = np.arange(0, duration, 1/fs)
    
    # Converte dB SPL para Pascal
    p_ref = 20e-6
    amplitude_pa = p_ref * 10**(amplitude_db / 20)
    
    # Aplica envelope para evitar cliques
    envelope = np.ones_like(t)
    ramp_samples = int(0.1 * duration * fs)  # 5ms de rampa
    envelope[:ramp_samples] = np.linspace(0, 1, ramp_samples)
    envelope[-ramp_samples:] = np.linspace(1, 0, ramp_samples)
    
    signal = amplitude_pa * np.sin(2 * np.pi * frequency * t) * envelope
    
    return signal

