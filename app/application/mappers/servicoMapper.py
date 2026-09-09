from app.domain.entities.servico import Servico
from app.application.dtos.servicoDto import ServicoResponseDTO


class ServicoMapper:
    @staticmethod
    def paraResponseDto(servico: Servico) -> ServicoResponseDTO:
        return ServicoResponseDTO(
            id=servico.id,
            nome=servico.nome,
            descricao=servico.descricao,
            duracaoMinutos=servico.duracaoMinutos,
            preco=servico.preco,
            ativo=servico.ativo,
        )
