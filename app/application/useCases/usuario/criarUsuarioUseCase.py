import bcrypt
from app.domain.entities.usuario import Usuario
from app.application.contracts.iUnitOfWork import IUnitOfWork
from app.domain.exceptions.validacaoError import ValidacaoError
from app.application.dtos.usuarioDto import CriarUsuarioDTO, UsuarioResponseDTO
from app.application.mappers.usuarioMapper import UsuarioMapper


class CriarUsuarioUseCase:
    def __init__(self, uow: IUnitOfWork):
        self._uow = uow

    async def executar(self, dto: CriarUsuarioDTO) -> UsuarioResponseDTO:
        async with self._uow as uow:
            if await uow.usuarios.buscarPorEmail(dto.email):
                raise ValidacaoError("E-mail já cadastrado")

            if await uow.usuarios.buscarPorCpf(dto.cpf):
                raise ValidacaoError("CPF já cadastrado")

            senhaHash = bcrypt.hashpw(dto.senha.encode(), bcrypt.gensalt()).decode()

            usuario = Usuario.criar(
                nome=dto.nome,
                email=dto.email,
                cpf=dto.cpf,
                senhaHash=senhaHash,
                tipos=dto.tipos,
            )

            salvo = await uow.usuarios.salvar(usuario)
            await uow.commit()
            return UsuarioMapper.paraResponseDto(salvo)
